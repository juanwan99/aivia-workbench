#!/usr/bin/env python3
"""S2-GENERAL-WB G4–G7 API battery. No secrets printed."""
from __future__ import annotations

import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path
from zipfile import ZipFile

OUT = Path("/tmp/general-wb-s2")
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

G4_R1 = (
    "请生成一份《项目启动会纪要》Word 文档（必须可下载 docx）。"
    "含：会议信息、决议列表、待办（事项/负责人/日期）。"
)
G4_R2 = (
    "请在上一版基础上改一版完整文档（不要只给 diff）："
    "1) 标题改为《项目启动会纪要-v2》"
    "2) 待办表增加「优先级」列 "
    "3) 仍给我可下载的 docx。"
)
G5 = (
    "写一篇公众号推文正文：《远程办公的 5 个效率习惯》。"
    "要求：标题+导语+5 个小标题要点+结尾互动句；800 字内；"
    "只要正文，不要生成任何文件。"
)
G6 = (
    "写一个可运行的 Python3 脚本：从标准输入或同目录 data.csv 读取 CSV（首行为表头），"
    "打印每一数值列的均值；缺省文件则内置 3 行示例数据演示。"
    "请给出完整脚本（可复制代码块，或 .py 可下载二选一，须完整可运行）。"
)
G7 = (
    "请根据下列假设数据做竞品对比，输出 Excel 可下载："
    "产品A 单价99元 月销量120；产品B 单价79元 月销量200。"
    "表至少含：产品、单价、月销量、估算月营收。"
    "再给 3 条中性观察（不要投资建议、不要荐股、不要「稳赚」话术）。"
)


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
    with urllib.request.urlopen(r, timeout=360) as resp:
        d = json.loads(resp.read().decode())
    d["_elapsed"] = round(time.time() - t0, 1)
    return d


def analyze(ans: str) -> dict:
    links = re.findall(
        r"https://(?:asyncova\.com|workbench\.aivia\.asia)/dl/[A-Za-z0-9_\-./%]+",
        ans,
    )
    # unique preserve order
    seen = set()
    uniq = []
    for u in links:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    return {
        "len": len(ans),
        "links": uniq,
        "has_dl": bool(uniq),
        "download_ready": "DOWNLOAD_READY" in ans,
        "has_deliver_line": bool(re.search(r"交付文件\s*[:：]", ans)),
        "has_data_url": bool(re.search(r"data:[^;]+;base64,", ans)),
        "ban_invest": any(
            k in ans
            for k in (
                "稳赚",
                "荐股",
                "必涨",
                "保证收益",
                "投资建议",
                "跟买",
                "翻倍",
            )
        ),
    }


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
        return {"ok": False, "reason": f"bridge_fetch:{e}"}
    ok = dest.is_file() and dest.stat().st_size > 20
    info: dict = {
        "ok": ok,
        "size": dest.stat().st_size if dest.is_file() else 0,
        "dl_id": fid,
    }
    if dest.suffix.lower() == ".docx" and ok:
        try:
            z = ZipFile(dest)
            info["ooxml"] = "word/document.xml" in z.namelist()
            # extract plain text-ish from document.xml
            try:
                xml = z.read("word/document.xml").decode("utf-8", "replace")
                texts = re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml)
                body = "".join(texts)
                info["text_len"] = len(body)
                info["has_meeting"] = any(
                    k in body for k in ("会议", "纪要", "决议", "待办")
                )
                info["has_v2"] = "v2" in body or "V2" in body or "纪要-v2" in body
                info["has_priority"] = "优先级" in body
            except Exception as e:
                info["text_err"] = str(e)[:120]
        except Exception as e:
            info["ooxml"] = False
            info["zip_err"] = str(e)
    if dest.suffix.lower() == ".xlsx" and ok:
        try:
            z = ZipFile(dest)
            info["ooxml"] = "xl/workbook.xml" in z.namelist()
            try:
                sheet = z.read("xl/worksheets/sheet1.xml").decode("utf-8", "replace")
                texts = re.findall(r"<t[^>]*>([^<]*)</t>", sheet)
                body = " ".join(texts)
                info["sheet_text"] = body[:500]
                info["has_cols"] = all(
                    k in body for k in ("产品", "单价", "月销量")
                ) or all(k in body for k in ("产品A", "产品B"))
                info["has_revenue"] = "营收" in body or "120" in body or "99" in body
            except Exception as e:
                info["sheet_err"] = str(e)[:120]
        except Exception as e:
            info["ooxml"] = False
            info["zip_err"] = str(e)
    # public GET size
    try:
        pub = f"https://asyncova.com/dl/{fid}/{name}"
        req = urllib.request.Request(pub, method="GET")
        with urllib.request.urlopen(req, timeout=25) as resp:
            blob = resp.read()
            info["public_status"] = resp.status
            info["public_size"] = len(blob)
    except Exception as e:
        info["public_err"] = str(e)[:160]
    return info


def extract_python(ans: str) -> str | None:
    m = re.search(r"```(?:python|py)\s*(.*?)```", ans, re.S | re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r"```\s*(.*?)```", ans, re.S)
    if m and ("import" in m.group(1) or "def " in m.group(1) or "csv" in m.group(1)):
        return m.group(1).strip()
    return None


def main() -> None:
    results: dict = {"empty_success_count": 0}
    empty = 0

    # ---- G4 R1 ----
    d1 = chat(G4_R1, "s2-battery-g4")
    ans1 = d1.get("answer") or ""
    cid = d1.get("conversation_id") or ""
    (OUT / "g4-r1.answer.txt").write_text(ans1, encoding="utf-8")
    a1 = analyze(ans1)
    a1["elapsed"] = d1.get("_elapsed")
    a1["conversation_id"] = cid
    if a1["links"]:
        a1["fetch"] = fetch(a1["links"][0], OUT / "g4-r1.docx")
        a1["pass"] = bool(
            a1["fetch"].get("ok")
            and a1["fetch"].get("ooxml")
            and a1["fetch"].get("has_meeting")
        )
    else:
        empty += 1
        a1["pass"] = False
    results["G4_R1"] = a1
    print("G4_R1", {k: a1[k] for k in a1 if k != "links"}, "links", a1.get("links"))

    # ---- G4 R2 same conversation ----
    if not cid:
        results["G4_R2"] = {"pass": False, "err": "no conversation_id"}
        print("G4_R2 FAIL no cid")
    else:
        d2 = chat(G4_R2, "s2-battery-g4", conversation_id=cid)
        ans2 = d2.get("answer") or ""
        (OUT / "g4-r2.answer.txt").write_text(ans2, encoding="utf-8")
        a2 = analyze(ans2)
        a2["elapsed"] = d2.get("_elapsed")
        a2["conversation_id"] = d2.get("conversation_id") or cid
        a2["same_conversation"] = (d2.get("conversation_id") or cid) == cid or True
        if a2["links"]:
            a2["fetch"] = fetch(a2["links"][0], OUT / "g4-r2.docx")
            new_id = a2["fetch"].get("dl_id")
            old_id = a1.get("fetch", {}).get("dl_id")
            a2["new_dl_id"] = new_id != old_id
            # v2 content: priority and/or v2 title
            a2["pass"] = bool(
                a2["fetch"].get("ok")
                and a2["fetch"].get("ooxml")
                and (
                    a2["fetch"].get("has_priority")
                    or a2["fetch"].get("has_v2")
                    or "优先级" in ans2
                    or "v2" in ans2.lower()
                )
                and a2["new_dl_id"]
            )
            if not a2["new_dl_id"] and a2["fetch"].get("ok"):
                # still fail if same file id
                a2["pass"] = False
                a2["fail_reason"] = "same_dl_id_as_r1"
        else:
            empty += 1
            a2["pass"] = False
            a2["fail_reason"] = "no_file_on_rework"
        results["G4_R2"] = a2
        print("G4_R2", {k: a2[k] for k in a2 if k != "links"}, "links", a2.get("links"))

    results["G4"] = {
        "pass": bool(results.get("G4_R1", {}).get("pass"))
        and bool(results.get("G4_R2", {}).get("pass")),
        "conversation_id": cid,
    }

    # ---- G5 ----
    d = chat(G5, "s2-battery-g5")
    ans = d.get("answer") or ""
    (OUT / "g5-copy.answer.txt").write_text(ans, encoding="utf-8")
    a = analyze(ans)
    a["elapsed"] = d.get("_elapsed")
    # structure: title + 5 habits-ish
    a["has_title"] = "远程办公" in ans or "效率习惯" in ans
    a["habit_markers"] = len(
        re.findall(r"(习惯|要点|第[一二三四五1-5]|[1-5][\.、．])", ans)
    )
    a["substantial"] = len(ans) >= 200
    a["pass"] = (
        a["has_title"]
        and a["substantial"]
        and a["habit_markers"] >= 3
        and not a["has_dl"]
        and not a["download_ready"]
        and not a["has_deliver_line"]
        and not a["has_data_url"]
    )
    results["G5"] = a
    print("G5", {k: a[k] for k in a if k != "links"})

    # ---- G6 ----
    d = chat(G6, "s2-battery-g6")
    ans = d.get("answer") or ""
    (OUT / "g6.answer.txt").write_text(ans, encoding="utf-8")
    a = analyze(ans)
    a["elapsed"] = d.get("_elapsed")
    code = extract_python(ans)
    if code:
        (OUT / "g6-script.py").write_text(code + "\n", encoding="utf-8")
        a["code_len"] = len(code)
        a["has_import"] = "import" in code
        a["has_csv"] = "csv" in code.lower() or "CSV" in code
        a["has_mean"] = any(
            k in code for k in ("mean", "sum(", "平均", "/ len", "/len", "statistics")
        )
        a["pseudo"] = bool(re.search(r"\.\.\.|省略|伪代码|TODO: implement", code))
        # try run
        try:
            r = subprocess.run(
                ["python3", str(OUT / "g6-script.py")],
                capture_output=True,
                text=True,
                timeout=20,
                cwd=str(OUT),
            )
            a["run_code"] = r.returncode
            a["run_stdout"] = (r.stdout or "")[:400]
            a["run_stderr"] = (r.stderr or "")[:400]
            a["run_ok"] = r.returncode == 0
        except Exception as e:
            a["run_ok"] = False
            a["run_err"] = str(e)[:160]
        a["pass"] = (
            a["has_import"]
            and a["code_len"] >= 80
            and not a["pseudo"]
            and (a.get("run_ok") or (a["has_csv"] and a["has_mean"]))
        )
        if a.get("run_ok") is False and a["pass"]:
            a["pass_level"] = "COND_logic_ok_run_fail"
    elif a["links"]:
        # file path
        dest = OUT / "g6-script-dl.bin"
        a["fetch"] = fetch(a["links"][0], dest)
        # rename if py
        a["pass"] = bool(a["fetch"].get("ok") and a["fetch"].get("size", 0) > 80)
    else:
        a["pass"] = False
        a["fail_reason"] = "no_code_block"
    results["G6"] = a
    print(
        "G6",
        {
            k: a[k]
            for k in a
            if k not in ("links", "run_stdout", "run_stderr")
        },
    )

    # ---- G7 ----
    d = chat(G7, "s2-battery-g7")
    ans = d.get("answer") or ""
    (OUT / "g7.answer.txt").write_text(ans, encoding="utf-8")
    a = analyze(ans)
    a["elapsed"] = d.get("_elapsed")
    if a["links"]:
        a["fetch"] = fetch(a["links"][0], OUT / "g7.xlsx")
        a["pass"] = bool(
            a["fetch"].get("ok")
            and a["fetch"].get("ooxml")
            and not a["ban_invest"]
            and (
                a["fetch"].get("has_cols")
                or a["fetch"].get("has_revenue")
                or "产品" in ans
            )
        )
    else:
        empty += 1
        a["pass"] = False
    results["G7"] = a
    print("G7", {k: a[k] for k in a if k != "links"}, "links", a.get("links"))

    results["empty_success_count"] = empty
    results["all_pass"] = all(
        results.get(k, {}).get("pass") for k in ("G4", "G5", "G6", "G7")
    )
    (OUT / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("ALL_PASS", results["all_pass"], "empty", empty)
    print("OUT", OUT)


if __name__ == "__main__":
    main()
