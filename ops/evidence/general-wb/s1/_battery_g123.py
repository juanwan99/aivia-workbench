#!/usr/bin/env python3
"""S1-GENERAL-WB G1/G2/G3 battery. Secrets not printed."""
from __future__ import annotations

import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path
from zipfile import ZipFile

OUT = Path("/tmp/general-wb-s1")
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
PUBLIC_BASES = (
    "https://asyncova.com/dl/",
    "https://workbench.aivia.asia/dl/",
)


def chat(query: str, user: str) -> dict:
    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "user": user,
    }
    data = json.dumps(payload).encode()
    r = urllib.request.Request(
        BASE + "/chat-messages",
        data=data,
        headers={"Authorization": f"Bearer {TOK}", "Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    with urllib.request.urlopen(r, timeout=300) as resp:
        d = json.loads(resp.read().decode())
    d["_elapsed"] = round(time.time() - t0, 1)
    return d


def analyze(ans: str) -> dict:
    links = re.findall(
        r"https://(?:asyncova\.com|workbench\.aivia\.asia)/dl/[A-Za-z0-9_\-./%]+",
        ans,
    )
    return {
        "len": len(ans),
        "links": links,
        "has_dl": bool(links),
        "download_ready": "DOWNLOAD_READY" in ans,
        "has_deliver_line": bool(re.search(r"交付文件\s*[:：]", ans)),
        "has_data_url": bool(re.search(r"data:[^;]+;base64,", ans)),
        "mentions_jiaoyan_only": "仅教研" in ans,
        "edu_main_narrative": any(
            k in ans for k in ("课件助手", "教案专员", "仅教研", "五教研")
        ),
    }


def fetch(url: str, dest: Path) -> dict:
    m = re.search(r"/dl/([a-f0-9]+)/([^?\s]+)", url)
    if not m:
        return {"ok": False, "reason": "no_id"}
    fid, name = m.group(1), m.group(2)
    # Prefer bridge localhost (works even if public edge flaky from ECS)
    try:
        subprocess.check_call(
            "docker exec aivia-bridge python -c "
            f"\"import urllib.request;open('/tmp/art','wb').write(urllib.request.urlopen('http://127.0.0.1:18090/dl/{fid}/{name}',timeout=30).read())\"",
            shell=True,
        )
        subprocess.check_call(f"docker cp aivia-bridge:/tmp/art {dest}", shell=True)
    except Exception as e:
        return {"ok": False, "reason": f"bridge_fetch:{e}"}
    ok = dest.is_file() and dest.stat().st_size > 20
    info: dict = {"ok": ok, "size": dest.stat().st_size if dest.is_file() else 0}
    if dest.suffix.lower() == ".docx" and ok:
        try:
            z = ZipFile(dest)
            info["ooxml"] = "word/document.xml" in z.namelist()
        except Exception as e:
            info["ooxml"] = False
            info["zip_err"] = str(e)
    if dest.suffix.lower() == ".xlsx" and ok:
        try:
            z = ZipFile(dest)
            info["ooxml"] = "xl/workbook.xml" in z.namelist()
        except Exception as e:
            info["ooxml"] = False
            info["zip_err"] = str(e)
    # also probe public URL headers if present
    for base in PUBLIC_BASES:
        if url.startswith(base) or True:
            pub = f"https://asyncova.com/dl/{fid}/{name}"
            try:
                req = urllib.request.Request(pub, method="GET")
                with urllib.request.urlopen(req, timeout=20) as resp:
                    info["public_asyncova_status"] = resp.status
                    info["public_asyncova_len"] = resp.headers.get("Content-Length")
                    info["public_asyncova_cd"] = resp.headers.get("Content-Disposition")
            except Exception as e:
                info["public_asyncova_err"] = str(e)[:160]
            break
    return info


def main() -> None:
    results: dict = {}
    empty = 0

    # W0 live parameters via parameters endpoint if available
    try:
        r = urllib.request.Request(
            BASE + "/parameters",
            headers={"Authorization": f"Bearer {TOK}"},
        )
        with urllib.request.urlopen(r, timeout=30) as resp:
            params = json.loads(resp.read().decode())
        (OUT / "parameters.json").write_text(
            json.dumps(
                {
                    "opening_statement": params.get("opening_statement"),
                    "suggested_questions": params.get("suggested_questions"),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        sq = params.get("suggested_questions") or []
        opening = params.get("opening_statement") or ""
        results["W0"] = {
            "suggested_count": len(sq),
            "suggested": sq,
            "opening": opening,
            "has_jinyanjiao": "仅教研" in opening or any("仅教研" in str(x) for x in sq),
            "edu_main": any(
                k in opening for k in ("课件助手", "HTML 课件", "Word 教案", "仅教研")
            ),
            "general_signals": sum(
                1
                for k in ("通用", "办公", "Word", "Excel", "公众号", "代码", "改稿", "分析")
                if k in opening
            ),
            "pass": len(sq) >= 6
            and "仅教研" not in opening
            and not any("仅教研" in str(x) for x in sq)
            and ("通用" in opening or "办公" in opening),
        }
    except Exception as e:
        results["W0"] = {"pass": False, "err": str(e)[:200]}

    # G1 Word
    d = chat(
        "请生成一份《Q3 项目周报》Word 文档，必须 docx 可下载。含：本周进展、风险、下周计划。",
        "s1-general-g1-docx",
    )
    ans = d.get("answer") or ""
    (OUT / "g1-docx.answer.txt").write_text(ans, encoding="utf-8")
    a = analyze(ans)
    a["elapsed"] = d.get("_elapsed")
    if a["links"]:
        a["fetch"] = fetch(a["links"][0], OUT / "g1-docx.docx")
        a["pass"] = bool(
            a["fetch"].get("ok") and a["fetch"].get("ooxml") is not False
        )
    else:
        empty += 1
        a["pass"] = False
    results["G1"] = a
    print("G1", {k: a[k] for k in a if k != "links"}, "links", a.get("links"))

    # G2 Excel
    d = chat(
        "请做一份《本周任务进度表》Excel，要能下载。列：任务、负责人、状态、截止日期；至少 4 行数据。",
        "s1-general-g2-xlsx",
    )
    ans = d.get("answer") or ""
    (OUT / "g2-xlsx.answer.txt").write_text(ans, encoding="utf-8")
    a = analyze(ans)
    a["elapsed"] = d.get("_elapsed")
    if a["links"]:
        a["fetch"] = fetch(a["links"][0], OUT / "g2-xlsx.xlsx")
        a["pass"] = bool(
            a["fetch"].get("ok") and a["fetch"].get("ooxml") is not False
        )
    else:
        empty += 1
        a["pass"] = False
    results["G2"] = a
    print("G2", {k: a[k] for k in a if k != "links"}, "links", a.get("links"))

    # G3 short answer — no fake download
    d = chat("只要短答：1+1等于几？不要文件。", "s1-general-g3-short")
    ans = d.get("answer") or ""
    (OUT / "g3-short.answer.txt").write_text(ans, encoding="utf-8")
    a = analyze(ans)
    a["elapsed"] = d.get("_elapsed")
    a["has_2"] = "2" in ans
    a["empty_success"] = bool(
        re.search(r"已完成|成功", ans)
        and not a["has_dl"]
        and len(ans.strip()) < 8
    )
    # PASS: answers, no /dl, no DOWNLOAD_READY, no 交付文件
    a["pass"] = (
        a["has_2"]
        and not a["has_dl"]
        and not a["download_ready"]
        and not a["has_deliver_line"]
        and not a["empty_success"]
    )
    results["G3"] = a
    print("G3", a)

    results["empty_success_count"] = empty
    results["all_pass"] = all(
        results.get(k, {}).get("pass") for k in ("W0", "G1", "G2", "G3")
    )
    (OUT / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("ALL_PASS", results["all_pass"])
    print("OUT", OUT)


if __name__ == "__main__":
    main()
