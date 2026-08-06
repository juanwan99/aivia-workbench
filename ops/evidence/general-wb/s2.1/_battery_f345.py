#!/usr/bin/env python3
"""S2.1 F3 G7 + F4 G4 filename regression. No secrets printed."""
from __future__ import annotations

import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path
from zipfile import ZipFile

OUT = Path("/tmp/general-wb-s2.1")
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

G7 = (
    "请根据下列假设数据做竞品对比，输出 Excel 可下载：产品A 单价99元 月销量120；"
    "产品B 单价79元 月销量200。表至少含：产品、单价、月销量、估算月营收。"
    "再在正文给出 3 条中性观察（编号1.2.3.）。不要投资建议、不要荐股、不要「稳赚」话术。"
    "交付文件：表格-竞品对比.xlsx"
)
G4 = "请生成《项目启动会纪要》Word 可下载。交付文件：文档-项目启动会纪要.docx"


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
    with urllib.request.urlopen(r, timeout=360) as resp:
        d = json.loads(resp.read().decode())
    d["_elapsed"] = round(time.time() - t0, 1)
    return d


def links(ans: str):
    return re.findall(
        r"https://(?:asyncova\.com|workbench\.aivia\.asia)/dl/[A-Za-z0-9_\-./%]+",
        ans,
    )


def fetch(url: str, dest: Path) -> dict:
    m = re.search(r"/dl/([a-f0-9]+)/([^?\s]+)", url)
    if not m:
        return {"ok": False}
    fid, name = m.group(1), m.group(2)
    subprocess.check_call(
        "docker exec aivia-bridge python -c "
        f"\"import urllib.request;open('/tmp/art','wb').write(urllib.request.urlopen('http://127.0.0.1:18090/dl/{fid}/{name}',timeout=30).read())\"",
        shell=True,
    )
    subprocess.check_call(f"docker cp aivia-bridge:/tmp/art {dest}", shell=True)
    ok = dest.is_file() and dest.stat().st_size > 20
    info = {"ok": ok, "size": dest.stat().st_size if ok else 0, "url_name": name}
    # Content-Disposition from public
    try:
        req = urllib.request.Request(
            f"https://asyncova.com/dl/{fid}/{name}", method="GET"
        )
        with urllib.request.urlopen(req, timeout=25) as resp:
            info["public_status"] = resp.status
            info["cd"] = resp.headers.get("Content-Disposition") or ""
            info["public_size"] = len(resp.read())
    except Exception as e:
        info["public_err"] = str(e)[:160]
    if dest.suffix.lower() == ".docx" and ok:
        try:
            z = ZipFile(dest)
            info["ooxml"] = "word/document.xml" in z.namelist()
        except Exception:
            info["ooxml"] = False
    if dest.suffix.lower() == ".xlsx" and ok:
        try:
            z = ZipFile(dest)
            info["ooxml"] = "xl/workbook.xml" in z.namelist()
        except Exception:
            info["ooxml"] = False
    return info


def display_name(ans: str, fetch_info: dict) -> str:
    # Prefer markdown table filename or bold 文件名
    m = re.search(r"\*\*文件名\*\*[：:]\s*(\S+)", ans)
    if m:
        return m.group(1)
    m = re.search(r"文件名[：:]\s*(\S+)", ans)
    if m:
        return m.group(1)
    m = re.search(r"点击下载\s+(\S+\.(?:docx|xlsx|html|md))", ans)
    if m:
        return m.group(1)
    cd = fetch_info.get("cd") or ""
    m = re.search(r"filename\*=UTF-8''([^;\s]+)", cd)
    if m:
        from urllib.parse import unquote

        return unquote(m.group(1))
    m = re.search(r'filename="([^"]+)"', cd)
    if m:
        return m.group(1)
    return fetch_info.get("url_name") or ""


def main() -> None:
    results = {}

    # F3 G7
    d = chat(G7, "s2.1-battery-g7")
    ans = d.get("answer") or ""
    (OUT / "g7.answer.txt").write_text(ans, encoding="utf-8")
    ls = links(ans)
    a = {
        "len": len(ans),
        "links": ls,
        "has_dl": bool(ls),
        "download_ready": "DOWNLOAD_READY" in ans,
        "elapsed": d.get("_elapsed"),
        "ban_invest": any(
            k in ans for k in ("稳赚", "荐股", "保证收益", "投资建议")
        ),
    }
    if ls:
        a["fetch"] = fetch(ls[0], OUT / "g7.xlsx")
        a["display_name"] = display_name(ans, a["fetch"])
    # assert script
    r = subprocess.run(
        ["python3", "/tmp/_assert_g7_obs.py", str(OUT / "g7.answer.txt")],
        capture_output=True,
        text=True,
    )
    a["assert_exit"] = r.returncode
    a["assert_out"] = (r.stdout or "").strip()
    a["pass"] = (
        r.returncode == 0
        and a.get("fetch", {}).get("ok")
        and a.get("fetch", {}).get("ooxml")
        and not a["ban_invest"]
    )
    results["F3_G7"] = a
    print("F3", a)

    # F4 G4 filename
    d = chat(G4, "s2.1-battery-g4")
    ans = d.get("answer") or ""
    (OUT / "g4.answer.txt").write_text(ans, encoding="utf-8")
    ls = links(ans)
    a = {
        "len": len(ans),
        "links": ls,
        "elapsed": d.get("_elapsed"),
    }
    if ls:
        a["fetch"] = fetch(ls[0], OUT / "g4.docx")
        a["display_name"] = display_name(ans, a["fetch"])
    name = a.get("display_name") or ""
    a["is_jiaoan"] = name == "教案.docx" or name.endswith("教案.docx")
    a["has_doc_hint"] = any(k in name for k in ("文档", "纪要", "项目"))
    a["pass"] = bool(
        a.get("fetch", {}).get("ok")
        and a.get("fetch", {}).get("ooxml")
        and not a["is_jiaoan"]
        and (a["has_doc_hint"] or "docx" in name.lower())
    )
    results["F4_G4"] = a
    print("F4", a)

    results["all_pass"] = bool(results["F3_G7"]["pass"] and results["F4_G4"]["pass"])
    (OUT / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("ALL_PASS", results["all_pass"])


if __name__ == "__main__":
    main()
