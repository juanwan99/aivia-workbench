#!/usr/bin/env python3
"""F3: ops smoke + TLS notes + bridge version."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

OUT = Path("/tmp/wb-fix-deploy-f3")
OUT.mkdir(parents=True, exist_ok=True)

# health
h = subprocess.check_output(
    [
        "docker",
        "exec",
        "aivia-bridge",
        "python",
        "-c",
        "import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:18090/health',timeout=5).read().decode())",
    ],
    text=True,
)
(OUT / "health.json").write_text(h.strip(), encoding="utf-8")
print("health", h.strip()[:250])
hj = json.loads(h)

# ops token
env = Path.home().joinpath(".secrets/bridge.env").read_text()
tok = ""
for line in env.splitlines():
    if "TOKEN" in line and "=" in line:
        k, v = line.split("=", 1)
        if "DL_PUT" in k or "OPS" in k:
            tok = v.strip().strip('"')
            if "DL_PUT" in k:
                break

def ops(path: str, method="GET", data=None):
    script = f"""
import json,urllib.request
body=None if {data!r} is None else json.dumps({data!r}).encode()
req=urllib.request.Request('http://127.0.0.1:18090{path}',data=body,headers={{'Content-Type':'application/json','X-Aivia-Ops':{tok!r}}},method='{method}')
print(urllib.request.urlopen(req,timeout=15).read().decode())
"""
    return subprocess.check_output(
        ["docker", "exec", "aivia-bridge", "python", "-c", script], text=True
    )

m = ops("/ops/metrics")
p = ops("/ops/policy")
(OUT / "metrics.json").write_text(m, encoding="utf-8")
(OUT / "policy.json").write_text(p, encoding="utf-8")
print("metrics_ok", "empty_success" in m)
print("policy_ok", "write-deny" in p)

# TLS from server
tls = subprocess.check_output(
    "echo | openssl s_client -connect workbench.aivia.asia:443 -servername workbench.aivia.asia 2>/dev/null | openssl x509 -noout -subject -issuer -dates 2>/dev/null; "
    "curl -skI --max-time 15 https://workbench.aivia.asia/ | head -15; "
    "curl -sI --max-time 15 https://workbench.aivia.asia/ 2>&1 | head -10",
    shell=True,
    text=True,
)
(OUT / "tls.txt").write_text(tls, encoding="utf-8")
print("tls_head", tls[:400].replace("\n", " | "))

# container
meta = subprocess.check_output(
    "docker inspect aivia-bridge --format 'id={{.Id}} status={{.State.Status}} image={{.Config.Image}}'; "
    "grep -n 'VERSION' /home/ops/aivia-workbench/bridge/server.py | head -2",
    shell=True,
    text=True,
)
(OUT / "bridge-deploy.txt").write_text(meta, encoding="utf-8")

# note known edge: client schannel
(OUT / "tls-edge-note.txt").write_text(
    "Source station (ECS openssl/curl -k/-s): see tls.txt. "
    "Some Windows client schannel paths may fail handshake (proxy/edge); "
    "server-side HTTPS /dl verified 200 attachment. Do not claim zero client TLS issues.\n",
    encoding="utf-8",
)
print("DONE", OUT, "version", hj.get("version"))
