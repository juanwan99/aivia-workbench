#!/usr/bin/env python3
"""Q2 expert battery: ≥2 cards real deliverables via Dify public chat API."""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

APP_ID = "fc3e14da-2861-4009-a888-730a6b993011"
BASE = os.environ.get("AIVIA_PUBLIC_BASE", "https://asyncova.com").rstrip("/")
# Prefer edge; allow override to local tunnel
API = f"{BASE}/v1/chat-messages"
OUT = Path(os.environ.get("QUAD_OUT", "/tmp/quad-launch-q2"))
OUT.mkdir(parents=True, exist_ok=True)

CASES = [
    {
        "id": "html-courseware",
        "query": "请做一份初中生物「豌豆杂交」HTML 课件，要能下载。标题写清。",
        "want_download": True,
        "exts": (".html",),
    },
    {
        "id": "lesson-docx",
        "query": "写一份初中生物细胞结构第一课时教案，Word 可下载。",
        "want_download": True,
        "exts": (".docx", ".doc"),
    },
]


def load_app_token() -> str:
    # api_tokens table via docker
    import subprocess

    sql = (
        "select token from api_tokens where app_id='%s' "
        "and type in ('app','api') order by created_at desc limit 1;"
        % APP_ID
    )
    cmd = [
        "docker",
        "exec",
        "dify-db_postgres-1",
        "psql",
        "-U",
        "postgres",
        "-d",
        "dify",
        "-tAc",
        sql,
    ]
    tok = subprocess.check_output(cmd, text=True).strip()
    if not tok:
        raise SystemExit("no app api token")
    return tok


def chat(token: str, query: str) -> str:
    body = json.dumps(
        {
            "inputs": {},
            "query": query,
            "response_mode": "blocking",
            "user": "quad-launch-q2",
        }
    ).encode()
    req = urllib.request.Request(
        API,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {e.code}: {err[:500]}") from e
    return data.get("answer") or data.get("message") or json.dumps(data, ensure_ascii=False)[:4000]


def extract_dl(answer: str) -> list[str]:
    urls = re.findall(r"https?://[^\s\)\]\"']+/dl/[A-Za-z0-9]+/[^\s\)\]\"']+", answer)
    # also relative
    rel = re.findall(r"/dl/[A-Za-z0-9]+/[^\s\)\]\"']+", answer)
    for r in rel:
        urls.append(BASE + r)
    # dedupe
    seen = []
    for u in urls:
        u = u.rstrip(".,);")
        if u not in seen:
            seen.append(u)
    return seen


def download(url: str, dest: Path) -> tuple[int, str, int]:
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
        ctype = resp.headers.get("Content-Type", "")
        dest.write_bytes(data)
        return resp.status, ctype, len(data)


def main() -> int:
    token = load_app_token()
    results = []
    for case in CASES:
        print(f"== {case['id']} ==")
        answer = chat(token, case["query"])
        head = OUT / f"{case['id']}.answer.head.txt"
        head.write_text(answer[:4000], encoding="utf-8")
        urls = extract_dl(answer)
        ready = "DOWNLOAD_READY" in answer or bool(urls)
        item = {
            "id": case["id"],
            "ready": ready,
            "urls": urls,
            "answer_len": len(answer),
            "pass": False,
            "file": None,
            "bytes": 0,
        }
        if case["want_download"] and urls:
            url = urls[0]
            # prefer matching ext
            for u in urls:
                if any(u.lower().endswith(ext) or f"file{ext}" in u.lower() for ext in case["exts"]):
                    url = u
                    break
            ext = ".bin"
            for e in case["exts"]:
                if e in url.lower():
                    ext = e
                    break
            dest = OUT / f"{case['id']}{ext}"
            try:
                status, ctype, n = download(url, dest)
                item["file"] = str(dest)
                item["bytes"] = n
                item["ctype"] = ctype
                item["status"] = status
                item["pass"] = status == 200 and n > 200
            except Exception as ex:  # noqa: BLE001
                item["error"] = str(ex)
        elif not case["want_download"]:
            item["pass"] = "DOWNLOAD_READY" not in answer and not urls
        results.append(item)
        print(json.dumps(item, ensure_ascii=False, indent=2))
        time.sleep(1)

    meta = {
        "base": BASE,
        "api": API,
        "results": results,
        "pass_count": sum(1 for r in results if r["pass"]),
        "need": 2,
    }
    (OUT / "q2-meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print("META", json.dumps(meta, ensure_ascii=False))
    if meta["pass_count"] < 2:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
