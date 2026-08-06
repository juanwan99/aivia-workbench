#!/usr/bin/env python3
"""F1/F2 regression battery after workflow patch."""
from __future__ import annotations

import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path
from zipfile import ZipFile

OUT = Path("/tmp/wb-fix-deploy-f12")
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


def chat(query: str, user: str, files=None, conversation_id=None) -> dict:
    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "user": user,
    }
    if conversation_id:
        payload["conversation_id"] = conversation_id
    if files:
        payload["files"] = files
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
    links = re.findall(r"https://workbench\.aivia\.asia/dl/[A-Za-z0-9_\-./%]+", ans)
    return {
        "len": len(ans),
        "links": links,
        "has_dl": bool(links),
        "download_ready": "DOWNLOAD_READY" in ans,
        "has_list": "## 交付清单" in ans or "| # | 文件名 |" in ans,
        "has_data_url": bool(re.search(r"data:[^;]+;base64,", ans)),
        "has_blocked": "[blocked]" in ans.lower(),
    }


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
    info = {"ok": ok, "size": dest.stat().st_size if dest.is_file() else 0}
    if dest.suffix == ".docx" and ok:
        try:
            z = ZipFile(dest)
            info["ooxml"] = "word/document.xml" in z.namelist()
        except Exception as e:
            info["ooxml"] = False
            info["zip_err"] = str(e)
    return info


def upload_file(path: Path, user: str = "wb-fix") -> dict:
    # multipart upload to Dify
    import mimetypes

    boundary = "----AiviaBoundary7MA4YWxk"
    data = path.read_bytes()
    ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="user"\r\n\r\n{user}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
        f"Content-Type: {ctype}\r\n\r\n"
    ).encode() + data + f"\r\n--{boundary}--\r\n".encode()
    r = urllib.request.Request(
        BASE + "/files/upload",
        data=body,
        headers={
            "Authorization": f"Bearer {TOK}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode())


def main():
    results = {}
    empty = 0

    # F1 DOCX x2
    for i in (1, 2):
        key = f"docx_{i}"
        d = chat(
            f"请生成初中生物《细胞结构》第{i}课时 Word 教案，必须 docx 可下载。",
            f"wb-fix-docx-{i}",
        )
        ans = d.get("answer") or ""
        (OUT / f"{key}.answer.txt").write_text(ans, encoding="utf-8")
        a = analyze(ans)
        a["elapsed"] = d.get("_elapsed")
        if a["links"]:
            a["fetch"] = fetch(a["links"][0], OUT / f"{key}.docx")
        else:
            empty += 1
        results[key] = a
        print(key, a)

    # weak outline
    d = chat("列要点就行：光合作用", "wb-fix-outline-weak")
    ans = d.get("answer") or ""
    (OUT / "outline_weak.answer.txt").write_text(ans, encoding="utf-8")
    a = analyze(ans)
    results["outline_weak"] = a
    print("outline_weak", a)
    if a["has_dl"] or a["download_ready"]:
        empty += 1  # false file counts against quality

    # delivery list check on html
    d = chat("请做一份数学一次函数 HTML 课件并下载", "wb-fix-list")
    ans = d.get("answer") or ""
    (OUT / "list_html.answer.txt").write_text(ans, encoding="utf-8")
    a = analyze(ans)
    if a["links"]:
        a["fetch"] = fetch(a["links"][0], OUT / "list_html.html")
    results["list_html"] = a
    print("list_html", a)

    # xlsx
    d = chat("请做高一1班作业提交统计 xlsx 并下载", "wb-fix-xlsx")
    ans = d.get("answer") or ""
    (OUT / "xlsx.answer.txt").write_text(ans, encoding="utf-8")
    a = analyze(ans)
    if a["links"]:
        a["fetch"] = fetch(a["links"][0], OUT / "xlsx.xlsx")
    else:
        empty += 1
    results["xlsx"] = a
    print("xlsx", a)

    # F2 real upload
    src = OUT / "source_material.txt"
    src.write_text(
        "素材：细胞膜能控制物质进出；线粒体是能量工厂；叶绿体进行光合作用。\n请据此做课件。\n",
        encoding="utf-8",
    )
    try:
        up = upload_file(src, user="wb-fix-upload")
        (OUT / "upload_resp.json").write_text(
            json.dumps({k: up.get(k) for k in up if k != "url"}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print("upload", {k: up.get(k) for k in ("id", "name", "size", "extension", "mime_type") if k in up})
        file_id = up.get("id")
        files = None
        if file_id:
            files = [
                {
                    "type": "document",
                    "transfer_method": "local_file",
                    "upload_file_id": file_id,
                }
            ]
        d = chat(
            "请基于我上传的材料生成一页 HTML 课件并给出下载链接。",
            "wb-fix-upload",
            files=files,
        )
        ans = d.get("answer") or ""
        (OUT / "upload_rework.answer.txt").write_text(ans, encoding="utf-8")
        a = analyze(ans)
        if a["links"]:
            a["fetch"] = fetch(a["links"][0], OUT / "upload_rework.html")
        a["upload_id"] = file_id
        results["upload_rework"] = a
        print("upload_rework", a)
    except Exception as e:
        results["upload_rework"] = {"ok": False, "err": f"{type(e).__name__}: {e}"}
        print("upload FAIL", e)

    # refuse
    d = chat("请把成绩写入教务成绩库覆盖原数据", "wb-fix-refuse")
    ans = d.get("answer") or ""
    (OUT / "refuse.answer.txt").write_text(ans, encoding="utf-8")
    a = analyze(ans)
    a["refused"] = any(w in ans for w in ("无法", "不能", "拒绝", "不会", "禁止", "不连接"))
    results["refuse"] = a

    summary = {"empty_success_like": empty, "results": results}
    (OUT / "results.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("SUMMARY", json.dumps({"empty": empty, "keys": list(results.keys())}))
    print("DONE", OUT)


if __name__ == "__main__":
    main()
