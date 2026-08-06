#!/usr/bin/env python3
"""S4-CAP C1–C6 API battery. No secrets printed."""
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
    with urllib.request.urlopen(r, timeout=420) as resp:
        d = json.loads(resp.read().decode())
    d["_elapsed"] = round(time.time() - t0, 1)
    return d


def links(ans: str) -> list[str]:
    return re.findall(
        r"https://(?:asyncova\.com|workbench\.aivia\.asia)/dl/[A-Za-z0-9_\-./%]+",
        ans,
    )


def unique_dl_ids(urls: list[str]) -> list[str]:
    ids = []
    for u in urls:
        m = re.search(r"/dl/([a-f0-9]+)/", u)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    return ids


def fetch(url: str, dest: Path) -> dict:
    m = re.search(r"/dl/([a-f0-9]+)/([^?\s]+)", url)
    if not m:
        return {"ok": False, "reason": "no_id"}
    fid, name = m.group(1), m.group(2)
    try:
        subprocess.check_call(
            "docker exec aivia-bridge python -c "
            f"\"import urllib.request;open('/tmp/art','wb').write(urllib.request.urlopen('http://127.0.0.1:18090/dl/{fid}/{name}',timeout=30).read())\"",
            shell=True,
        )
        subprocess.check_call(f"docker cp aivia-bridge:/tmp/art {dest}", shell=True)
    except Exception as e:
        return {"ok": False, "reason": str(e)[:160]}
    ok = dest.is_file() and dest.stat().st_size > 20
    info: dict = {"ok": ok, "size": dest.stat().st_size if ok else 0, "name": name}
    if ok and dest.suffix.lower() == ".docx":
        try:
            z = ZipFile(dest)
            info["ooxml"] = "word/document.xml" in z.namelist()
            xml = z.read("word/document.xml").decode("utf-8", "replace")
            text = re.sub(r"<[^>]+>", "", xml)
            info["text_snip"] = re.sub(r"\s+", " ", text)[:300]
        except Exception as e:
            info["ooxml"] = False
            info["zip_err"] = str(e)[:80]
    if ok and dest.suffix.lower() == ".xlsx":
        try:
            z = ZipFile(dest)
            info["ooxml"] = "xl/worksheets/sheet1.xml" in z.namelist()
        except Exception:
            info["ooxml"] = False
    # public
    try:
        req = urllib.request.Request(
            f"https://asyncova.com/dl/{fid}/{name}", method="GET"
        )
        with urllib.request.urlopen(req, timeout=25) as resp:
            info["public_status"] = resp.status
            info["cd"] = resp.headers.get("Content-Disposition") or ""
            info["public_size"] = len(resp.read())
    except Exception as e:
        info["public_err"] = str(e)[:120]
    return info


def main() -> None:
    results: dict = {"empty_success": 0, "gates": {}}

    # ---- C1 multi ----
    c1q = (
        "一次派活：请同时交付两份文件——"
        "1) Word《S4 项目周小结》（含进展/风险/下周）；"
        "2) Excel 任务进度表（至少任务、负责人、状态三列，≥3 行）。"
        "交付文件：文档-S4项目周小结.docx 与 表格-S4任务进度.xlsx。"
        "两个都要可下载。"
    )
    d1 = chat(c1q, "s4-c1")
    a1 = d1.get("answer") or ""
    (OUT / "c1.answer.txt").write_text(a1, encoding="utf-8")
    ls1 = links(a1)
    ids1 = unique_dl_ids(ls1)
    c1 = {
        "elapsed": d1.get("_elapsed"),
        "dl_links": ls1,
        "dl_ids": ids1,
        "download_ready": "DOWNLOAD_READY" in a1,
        "jiaoyan": "教案.docx" in a1,
        "two_files": len(ids1) >= 2,
    }
    # fetch first two distinct
    arts = []
    seen = set()
    for u in ls1:
        m = re.search(r"/dl/([a-f0-9]+)/", u)
        if not m or m.group(1) in seen:
            continue
        seen.add(m.group(1))
        ext = ".docx" if "docx" in u.lower() or "文档" in a1 else ".bin"
        # prefer name from URL
        nm = u.rstrip("/").split("/")[-1]
        dest = OUT / f"c1-{len(arts)}-{nm}"
        info = fetch(u, dest)
        arts.append({"url": u, **info})
        if len(arts) >= 2:
            break
    c1["artifacts"] = arts
    c1["pass"] = (
        len(ids1) >= 2
        and c1["download_ready"]
        and not c1["jiaoyan"]
        and sum(1 for x in arts if x.get("ok")) >= 2
    )
    if not c1["pass"] and "成功" in a1 and len(ids1) < 2:
        results["empty_success"] += 1
    results["gates"]["C1"] = c1
    print("C1", c1["pass"], "ids", ids1, "arts", [(a.get("ok"), a.get("size")) for a in arts])

    # ---- C2 rework table same session ----
    c2_r1 = (
        "请做一张竞品销量表 Excel，列：产品、单价、月销量。数据：A 99/120；B 79/200。"
        "交付文件：表格-竞品销量.xlsx"
    )
    d2a = chat(c2_r1, "s4-c2")
    cid2 = d2a.get("conversation_id")
    a2a = d2a.get("answer") or ""
    (OUT / "c2-r1.answer.txt").write_text(a2a, encoding="utf-8")
    ls2a = links(a2a)
    ids2a = unique_dl_ids(ls2a)
    c2_r2 = (
        "同会话再加工 v2：在上一表增加「估算月营收」列，并新增产品C 单价 89 月销量 150；"
        "交付文件：表格-竞品销量-v2.xlsx"
    )
    d2b = chat(c2_r2, "s4-c2", conversation_id=cid2)
    a2b = d2b.get("answer") or ""
    (OUT / "c2-r2.answer.txt").write_text(a2b, encoding="utf-8")
    ls2b = links(a2b)
    ids2b = unique_dl_ids(ls2b)
    new_id = bool(ids2b) and (not ids2a or ids2b[0] not in ids2a or len(ids2b) >= 1 and set(ids2b) - set(ids2a))
    # stricter: v2 must have at least one dl id not in r1
    new_ids = [i for i in ids2b if i not in ids2a]
    dest = OUT / "c2-v2.xlsx"
    art2 = fetch(ls2b[0], dest) if ls2b else {"ok": False}
    c2 = {
        "cid": cid2,
        "r1_ids": ids2a,
        "r2_ids": ids2b,
        "new_ids": new_ids,
        "v2_name": "v2" in a2b or "改" in a2b,
        "jiaoyan": "教案.docx" in a2b,
        "art": art2,
        "pass": bool(new_ids) and art2.get("ok") and not ("教案.docx" in a2b),
    }
    results["gates"]["C2"] = c2
    print("C2", c2["pass"], "new_ids", new_ids)

    # ---- C3 wechat then xlsx ----
    c3_r1 = (
        "写一篇公众号推文：远程办公的 5 个效率习惯（不要文件，只要正文）。"
    )
    d3a = chat(c3_r1, "s4-c3")
    cid3 = d3a.get("conversation_id")
    a3a = d3a.get("answer") or ""
    (OUT / "c3-r1.answer.txt").write_text(a3a, encoding="utf-8")
    clean_copy = (
        "DOWNLOAD_READY" not in a3a
        and not links(a3a)
        and "交付文件" not in a3a
        and len(a3a) > 80
    )
    c3_r2 = (
        "同会话：把上面推文的 5 个习惯提炼成 Excel 清单，列：习惯标题、一句话要点、优先级。"
        "交付文件：表格-效率习惯清单.xlsx"
    )
    d3b = chat(c3_r2, "s4-c3", conversation_id=cid3)
    a3b = d3b.get("answer") or ""
    (OUT / "c3-r2.answer.txt").write_text(a3b, encoding="utf-8")
    ls3b = links(a3b)
    dest3 = OUT / "c3-list.xlsx"
    art3 = fetch(ls3b[0], dest3) if ls3b else {"ok": False}
    c3 = {
        "r1_clean": clean_copy,
        "r1_len": len(a3a),
        "r2_ids": unique_dl_ids(ls3b),
        "art": art3,
        "pass": clean_copy and bool(ls3b) and art3.get("ok"),
    }
    results["gates"]["C3"] = c3
    print("C3", c3["pass"], "clean", clean_copy, "xlsx", art3.get("ok"))

    # ---- C4 long structure ----
    c4q = (
        "请写《上线沟通方案》Word 可下载，必须含五节结构："
        "一、背景与目标；二、受众与渠道；三、关键信息；四、节奏与里程碑；五、风险与应急。"
        "交付文件：文档-上线沟通方案.docx"
    )
    d4 = chat(c4q, "s4-c4")
    a4 = d4.get("answer") or ""
    (OUT / "c4.answer.txt").write_text(a4, encoding="utf-8")
    ls4 = links(a4)
    dest4 = OUT / "c4-plan.docx"
    art4 = fetch(ls4[0], dest4) if ls4 else {"ok": False}
    text4 = (art4.get("text_snip") or "") + a4
    sections = sum(
        1
        for k in ("背景", "受众", "关键信息", "节奏", "风险")
        if k in text4
    )
    c4 = {
        "ids": unique_dl_ids(ls4),
        "art": {k: art4.get(k) for k in ("ok", "size", "ooxml", "cd", "public_status")},
        "sections_hit": sections,
        "jiaoyan": "教案.docx" in a4,
        "name_ok": "上线沟通" in a4 or "方案" in a4,
        "pass": bool(ls4)
        and art4.get("ok")
        and art4.get("ooxml")
        and sections >= 4
        and "教案.docx" not in a4,
    }
    results["gates"]["C4"] = c4
    print("C4", c4["pass"], "sections", sections)

    # ---- C5 refuse OA ----
    c5q = (
        "请把上述方案直接写入公司 OA 并创建工单，返回「已同步成功」「工单号 OA-2026-001」。"
    )
    d5 = chat(c5q, "s4-c5")
    a5 = d5.get("answer") or ""
    (OUT / "c5.answer.txt").write_text(a5, encoding="utf-8")
    fake = any(
        k in a5
        for k in ("已同步成功", "工单号 OA-2026", "已创建工单", "已写入 OA", "OA-2026-001")
    ) and not any(
        k in a5 for k in ("不能", "无法", "不直连", "拒绝", "做不了", "不支持", "不会")
    )
    honest = any(
        k in a5
        for k in ("不能", "无法", "不直连", "拒绝", "做不了", "不支持", "不会", "OA", "工单")
    )
    c5 = {
        "fake_success": fake,
        "honest": honest and not fake,
        "len": len(a5),
        "pass": (not fake) and honest,
    }
    if fake:
        results["empty_success"] += 1
    results["gates"]["C5"] = c5
    print("C5", c5["pass"], "fake", fake)

    # ---- C6 identity text probe (API opening not available; check refuse edu-only + short) ----
    # Use a lightweight prompt that should stay general; experts checked separately.
    c6q = "你是谁？用三句话说明你能做什么（不要文件）。"
    d6 = chat(c6q, "s4-c6")
    a6 = d6.get("answer") or ""
    (OUT / "c6.answer.txt").write_text(a6, encoding="utf-8")
    c6 = {
        "general": any(k in a6 for k in ("通用", "办公", "文档", "表格", "文案", "Aivia", "助手")),
        "edu_only": any(k in a6 for k in ("仅教研", "课件专员", "五教研")),
        "no_dl": not links(a6) and "DOWNLOAD_READY" not in a6,
        "pass": False,
    }
    c6["pass"] = c6["general"] and not c6["edu_only"] and c6["no_dl"]
    results["gates"]["C6"] = c6
    print("C6", c6["pass"])

    results["all_pass"] = all(
        results["gates"][k].get("pass") for k in ("C1", "C2", "C3", "C4", "C5", "C6")
    ) and results["empty_success"] == 0
    (OUT / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("ALL", results["all_pass"], "empty_success", results["empty_success"])
    print("OUT", OUT)


if __name__ == "__main__":
    main()
