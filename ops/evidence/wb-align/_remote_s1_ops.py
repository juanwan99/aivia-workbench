#!/usr/bin/env python3
"""S1: exercise bridge ops metrics/audit/policy/quality + quota check."""
from __future__ import annotations

import json
import os
import subprocess
import urllib.request
from pathlib import Path

# load put token from server secrets without printing
env = {}
for line in Path.home().joinpath(".secrets/bridge.env").read_text().splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
TOK = env.get("BRIDGE_OPS_TOKEN") or env.get("BRIDGE_DL_PUT_TOKEN") or ""
print("ops_token_len", len(TOK))


def call(method: str, path: str, data=None):
    body = None if data is None else json.dumps(data).encode()
    r = urllib.request.Request(
        "http://127.0.0.1:18090" + path,
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Aivia-Ops": TOK,
            "X-Aivia-Dl-Put": TOK,
        },
        method=method,
    )
    # bridge may only listen inside container
    try:
        with urllib.request.urlopen(r, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except Exception as e:
        # fallback docker exec python
        payload = json.dumps(
            {
                "method": method,
                "path": path,
                "data": data,
                "tok": TOK,
            }
        )
        script = f"""
import json,urllib.request
cfg=json.loads({payload!r})
body=None if cfg['data'] is None else json.dumps(cfg['data']).encode()
req=urllib.request.Request('http://127.0.0.1:18090'+cfg['path'],data=body,headers={{'Content-Type':'application/json','X-Aivia-Ops':cfg['tok'],'X-Aivia-Dl-Put':cfg['tok']}},method=cfg['method'])
resp=urllib.request.urlopen(req,timeout=15)
print(resp.status)
print(resp.read().decode())
"""
        out = subprocess.check_output(
            ["docker", "exec", "aivia-bridge", "python", "-c", script],
            text=True,
        )
        lines = out.strip().split("\n", 1)
        return int(lines[0]), json.loads(lines[1])


def main():
    # health
    script = "import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:18090/health',timeout=5).read().decode())"
    health = subprocess.check_output(
        ["docker", "exec", "aivia-bridge", "python", "-c", script], text=True
    )
    print("health", health.strip()[:300])
    h = json.loads(health)
    assert h.get("version") == "0.2.2", h

    st, m = call("GET", "/ops/metrics")
    print("metrics", st, list((m.get("metrics") or m).keys())[:12])
    assert st == 200 and m.get("ok")

    st, a = call("GET", "/ops/audit/tail?n=20")
    print("audit", st, "events", len(a.get("events") or []))
    assert st == 200 and len(a.get("events") or []) >= 1

    st, p = call("GET", "/ops/policy")
    print("policy", st, (p.get("policy") or {}).get("name"))
    assert st == 200 and p.get("policy")

    # quality events: empty_success inject + refuse
    before = (m.get("metrics") or {}).get("empty_success", 0)
    st, q1 = call(
        "POST",
        "/ops/quality-event",
        {"kind": "empty_success", "case_id": "s1-inject", "note": "probe counter"},
    )
    print("quality empty", st, q1)
    st, q2 = call(
        "POST",
        "/ops/quality-event",
        {"kind": "refuse_write", "case_id": "s6", "note": "grade db refuse"},
    )
    print("quality refuse", st, q2)
    st, m2 = call("GET", "/ops/metrics")
    after = (m2.get("metrics") or {}).get("empty_success", 0)
    print("empty_success before/after", before, after)
    assert after >= before + 1

    # G-07 quota visible
    mm = m2.get("metrics") or {}
    print("dl_daily_max", mm.get("dl_daily_max"), "dl_put_today", mm.get("dl_put_today"))

    # desensitized evidence dump
    out = Path("/tmp/wb-align-s1")
    out.mkdir(exist_ok=True)
    (out / "health.json").write_text(json.dumps(h, indent=2), encoding="utf-8")
    (out / "metrics.json").write_text(json.dumps(m2, indent=2, ensure_ascii=False), encoding="utf-8")
    # redact nothing sensitive in audit sample (no tokens by design)
    (out / "audit-tail.json").write_text(json.dumps(a, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "policy.json").write_text(json.dumps(p, indent=2, ensure_ascii=False), encoding="utf-8")
    print("DONE", out)


if __name__ == "__main__":
    main()
