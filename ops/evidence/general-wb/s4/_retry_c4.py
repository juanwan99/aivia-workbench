#!/usr/bin/env python3
"""Retry C4 only after S4 pack plain-md fix."""
from __future__ import annotations

import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path
from zipfile import ZipFile

OUT = Path("/tmp/general-wb-s4")
OUT.mkdir(parents=True, exist_ok=True)
TOK = Path("/tmp/wb-align-app-key.txt").read_text().strip()
IP = (
    subprocess.check_output(
        [
            "docker",
            "inspect",
            "dify-api-1",
            "--format",
            "{{range .NetworkSettings.Networks}}{{.IPAddress}} {{end}}",
        ],
        text=True,
    )
    .strip()
    .split()[0]
)
BASE = f"http://{IP}:5001/v1"
Q = (
    "请写《上线沟通方案》Word 可下载，必须含五节结构："
    "一、背景与目标；二、受众与渠道；三、关键信息；四、节奏与里程碑；五、风险与应急。"
    "请用 markdown 代码块写出正文。交付文件：文档-上线沟通方案.docx"
)


def main() -> None:
    payload = {
        "inputs": {},
        "query": Q,
        "response_mode": "blocking",
        "user": "s4-c4-retry",
    }
    req = urllib.request.Request(
        BASE + "/chat-messages",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {TOK}", "Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=420) as resp:
        d = json.loads(resp.read().decode())
    a = d.get("answer") or ""
    (OUT / "c4.answer.txt").write_text(a, encoding="utf-8")
    links = re.findall(
        r"https://(?:asyncova\.com|workbench\.aivia\.asia)/dl/[A-Za-z0-9_\-./%]+",
        a,
    )
    print("elapsed", round(time.time() - t0, 1))
    print("links", links[:4])
    print("ready", "DOWNLOAD_READY" in a, "jiaoyan", "教案.docx" in a)
    print("fence", ("```markdown" in a) or ("```md" in a), "len", len(a))
    ok = False
    art = {}
    if links:
        m = re.search(r"/dl/([a-f0-9]+)/([^?\s]+)", links[0])
        fid, name = m.group(1), m.group(2)
        subprocess.check_call(
            "docker exec aivia-bridge python -c "
            f"\"import urllib.request;open('/tmp/art','wb').write(urllib.request.urlopen('http://127.0.0.1:18090/dl/{fid}/{name}',timeout=30).read())\"",
            shell=True,
        )
        dest = OUT / "c4-plan.docx"
        subprocess.check_call(f"docker cp aivia-bridge:/tmp/art {dest}", shell=True)
        z = ZipFile(dest)
        xml = z.read("word/document.xml").decode("utf-8", "replace")
        text = re.sub(r"<[^>]+>", "", xml)
        hits = {k: (k in text or k in a) for k in ("背景", "受众", "关键信息", "节奏", "风险")}
        art = {
            "ok": True,
            "size": dest.stat().st_size,
            "ooxml": "word/document.xml" in z.namelist(),
            "hits": hits,
            "cd_public": None,
        }
        try:
            with urllib.request.urlopen(
                f"https://asyncova.com/dl/{fid}/{name}", timeout=25
            ) as resp:
                art["public_status"] = resp.status
                art["cd"] = resp.headers.get("Content-Disposition") or ""
        except Exception as e:
            art["public_err"] = str(e)[:120]
        ok = art["ooxml"] and sum(hits.values()) >= 4 and "教案.docx" not in a
        print("art", art)
    print("C4_PASS", ok)
    # merge into results.json
    res_path = OUT / "results.json"
    if res_path.exists():
        results = json.loads(res_path.read_text(encoding="utf-8"))
    else:
        results = {"empty_success": 0, "gates": {}}
    results["gates"]["C4"] = {
        "ids": [
            re.search(r"/dl/([a-f0-9]+)/", u).group(1)
            for u in links
            if re.search(r"/dl/([a-f0-9]+)/", u)
        ],
        "art": art,
        "pass": ok,
        "jiaoyan": "教案.docx" in a,
    }
    results["all_pass"] = all(
        results.get("gates", {}).get(k, {}).get("pass")
        for k in ("C1", "C2", "C3", "C4", "C5", "C6")
    ) and results.get("empty_success", 0) == 0
    res_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ALL", results["all_pass"])


if __name__ == "__main__":
    main()
