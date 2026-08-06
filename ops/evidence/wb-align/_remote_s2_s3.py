#!/usr/bin/env python3
"""S2/S3 chat cases: docx, product list, templates, upload-ish, s7 fix attempt."""
from __future__ import annotations

import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path

OUT = Path("/tmp/wb-align-s2s3")
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


def chat(query: str, user: str, conversation_id: str | None = None) -> dict:
    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "user": user,
    }
    if conversation_id:
        payload["conversation_id"] = conversation_id
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
    d["_elapsed_s"] = round(time.time() - t0, 1)
    return d


def analyze(ans: str) -> dict:
    links = re.findall(r"https://workbench\.aivia\.asia/dl/[A-Za-z0-9_\-./%]+", ans)
    return {
        "answer_len": len(ans),
        "dl_links": links,
        "has_dl": bool(links),
        "has_data_url": bool(re.search(r"data:[^;]+;base64,", ans)),
        "download_ready": "DOWNLOAD_READY" in ans,
        "has_product_section": ("下载" in ans and "http" in ans) or "DOWNLOAD_READY" in ans,
    }


def fetch_dl(url: str, dest: Path) -> dict:
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
    return {"ok": dest.is_file(), "size": dest.stat().st_size}


def main():
    results = {}

    # S2: docx
    d = chat(
        "请生成初中生物《细胞结构》第一课时 Word 教案 docx，必须 https 下载链接。",
        "wb-align-s2-docx",
    )
    ans = d.get("answer") or ""
    (OUT / "s2_docx.answer.txt").write_text(ans, encoding="utf-8")
    a = analyze(ans)
    a["elapsed_s"] = d.get("_elapsed_s")
    if a["dl_links"]:
        a["dl_fetch"] = fetch_dl(a["dl_links"][0], OUT / "s2_docx.artifact.docx")
    results["s2_docx"] = a
    print("docx", a)

    # S2: product list / summary (three formats in one message style)
    d = chat(
        "请用清单形式交付：1) HTML课件下载 2) 说明完成状态与耗时感。生成一份简单HTML课件并下载。",
        "wb-align-s2-panel",
    )
    ans = d.get("answer") or ""
    (OUT / "s2_panel.answer.txt").write_text(ans, encoding="utf-8")
    a = analyze(ans)
    a["elapsed_s"] = d.get("_elapsed_s")
    results["s2_panel"] = a
    print("panel", a)

    # S3: scene entries via recommended-style prompts (4 scenes)
    scenes = [
        ("scene_html", "【场景：课件】生成数学一次函数 HTML 课件并下载"),
        ("scene_docx", "【场景：教案】生成物理浮力第一课时 Word 教案并下载"),
        ("scene_xlsx", "【场景：报表】生成初二3班课堂测验得分统计 xlsx 并下载"),
        ("scene_outline", "【场景：大纲】只要浮力课大纲，不要文件"),
    ]
    for key, q in scenes:
        d = chat(q, f"wb-align-{key}")
        ans = d.get("answer") or ""
        (OUT / f"{key}.answer.txt").write_text(ans, encoding="utf-8")
        a = analyze(ans)
        a["elapsed_s"] = d.get("_elapsed_s")
        if a["dl_links"] and key != "scene_outline":
            ext = ".html" if "html" in key else (".docx" if "docx" in key else ".xlsx")
            a["dl_fetch"] = fetch_dl(a["dl_links"][0], OUT / f"{key}.artifact{ext}")
        results[key] = a
        print(key, {k: a[k] for k in a if k != "dl_links"}, "links", a.get("dl_links", [])[:1])

    # S3: s7 chain stronger outline instruction
    d1 = chat("生成生物细胞结构 HTML 课件并下载", "wb-align-s7b")
    cid = d1.get("conversation_id")
    d2 = chat("再做班级作业提交 xlsx 表并下载", "wb-align-s7b", cid)
    d3 = chat(
        "现在只要本节课教学大纲文字要点，严禁输出任何下载链接或 DOWNLOAD_READY 或文件。",
        "wb-align-s7b",
        cid,
    )
    for name, d in [("s7b_a", d1), ("s7b_b", d2), ("s7b_c", d3)]:
        (OUT / f"{name}.answer.txt").write_text(d.get("answer") or "", encoding="utf-8")
    a1, a2, a3 = analyze(d1.get("answer") or ""), analyze(d2.get("answer") or ""), analyze(
        d3.get("answer") or ""
    )
    results["s7b"] = {
        "html_dl": a1["has_dl"],
        "xlsx_dl": a2["has_dl"],
        "outline_no_dl": not a3["has_dl"],
        "a3_sample": (d3.get("answer") or "")[:200],
    }
    print("s7b", results["s7b"])

    # C-01 upload: Dify file upload via API is multi-step; mark partial if only text-context file content
    d = chat(
        "下面是一段课文素材（当作已上传材料）：『细胞膜能控制物质进出』。请基于该素材生成一页 HTML 课件并下载。",
        "wb-align-c01",
    )
    ans = d.get("answer") or ""
    (OUT / "c01_rework.answer.txt").write_text(ans, encoding="utf-8")
    results["c01_rework"] = analyze(ans)
    print("c01", results["c01_rework"])

    # post quality events for real outcomes
    ops = Path.home().joinpath(".secrets/bridge.env").read_text()
    tok = ""
    for line in ops.splitlines():
        if line.startswith("BRIDGE_DL_PUT_TOKEN=") or line.startswith("BRIDGE_OPS_TOKEN="):
            tok = line.split("=", 1)[1].strip().strip('"')
            if "OPS" in line or not tok:
                continue
    for line in ops.splitlines():
        if "TOKEN" in line and "=" in line:
            k, v = line.split("=", 1)
            if "DL_PUT" in k or "OPS" in k:
                tok = v.strip().strip('"')
                break
    # quality via docker
    def qevent(kind, case):
        script = f"""
import json,urllib.request
body=json.dumps({{'kind':'{kind}','case_id':'{case}'}}).encode()
req=urllib.request.Request('http://127.0.0.1:18090/ops/quality-event',data=body,headers={{'Content-Type':'application/json','X-Aivia-Ops':{tok!r}}},method='POST')
print(urllib.request.urlopen(req,timeout=10).read().decode())
"""
        try:
            subprocess.check_call(["docker", "exec", "aivia-bridge", "python", "-c", script])
        except Exception as e:
            print("qevent fail", e)

    if results.get("s2_docx", {}).get("has_dl"):
        qevent("ok_file", "s2_docx")
    if results.get("scene_outline", {}).get("has_dl") is False:
        qevent("ok_outline", "scene_outline")
    if results.get("s7b", {}).get("outline_no_dl"):
        qevent("ok_outline", "s7b")
    else:
        qevent("fail", "s7b_outline_still_file")

    (OUT / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("DONE", OUT)


if __name__ == "__main__":
    main()
