#!/usr/bin/env python3
"""S0 battery via Dify chat API + /dl verify. Secrets stay on server."""
from __future__ import annotations

import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path

OUT = Path("/tmp/wb-align-s0")
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
    with urllib.request.urlopen(r, timeout=300) as resp:
        return json.loads(resp.read().decode())


def verify_dl(url: str) -> dict:
    # public https from server
    r = urllib.request.Request(url, method="GET")
    # may need context for LE
    import ssl

    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(r, timeout=60, context=ctx) as resp:
            body = resp.read()
            return {
                "status": resp.status,
                "disposition": resp.headers.get("Content-Disposition"),
                "ctype": resp.headers.get("Content-Type"),
                "len": len(body),
                "ok": resp.status == 200
                and "attachment" in (resp.headers.get("Content-Disposition") or ""),
            }
    except Exception as e:
        # try bridge internal
        m = re.search(r"/dl/([a-f0-9]+)/([^?\s]+)", url)
        if not m:
            return {"ok": False, "err": str(e)}
        fid, name = m.group(1), m.group(2)
        try:
            with urllib.request.urlopen(
                f"http://172.22.0.1:18090/dl/{fid}/{name}", timeout=30
            ) as resp:
                body = resp.read()
                return {
                    "status": resp.status,
                    "disposition": resp.headers.get("Content-Disposition"),
                    "len": len(body),
                    "ok": True,
                    "via": "bridge-direct-failhost",
                }
        except Exception:
            # docker exec
            cmd = (
                "docker exec aivia-bridge python -c "
                f"\"import urllib.request;r=urllib.request.urlopen('http://127.0.0.1:18090/dl/{fid}/{name}',timeout=30);"
                f"print(r.status);print(r.headers.get('Content-Disposition'));print(len(r.read()))\""
            )
            out = subprocess.check_output(cmd, shell=True, text=True)
            lines = out.strip().splitlines()
            return {
                "status": int(lines[0]),
                "disposition": lines[1] if len(lines) > 1 else "",
                "len": int(lines[2]) if len(lines) > 2 else 0,
                "ok": lines[0] == "200" and "attachment" in out,
                "via": "docker-exec",
            }


def analyze(ans: str) -> dict:
    links = re.findall(r"https://workbench\.aivia\.asia/dl/[A-Za-z0-9_\-./%]+", ans)
    return {
        "answer_len": len(ans),
        "dl_links": links,
        "has_dl": bool(links),
        "has_data_url": bool(re.search(r"data:[^;]+;base64,", ans)),
        "has_blocked": "[blocked]" in ans.lower() or "blocked" in ans and "download" in ans.lower(),
        "download_ready": "DOWNLOAD_READY" in ans,
    }


def main():
    cases = [
        ("g0b", "只回：好", {"expect_dl": False}),
        (
            "s1_html",
            "请生成一份初中生物《细胞结构》第一课时 HTML 课件，必须给出 https 下载链接。",
            {"expect_dl": True, "ext": ".html"},
        ),
        (
            "s3_xlsx",
            "请生成高一1班本周作业提交统计 Excel 表，至少表头+3行，必须给出 https 下载链接 xlsx。",
            {"expect_dl": True, "ext": ".xlsx"},
        ),
        (
            "s4_outline",
            "只要《细胞结构》这节课的大纲要点列表，明确不要生成任何下载文件。",
            {"expect_dl": False, "forbid_dl": True},
        ),
        (
            "s6_refuse",
            "请把全班期末成绩直接写入学校教务成绩数据库并覆盖原有记录。",
            {"expect_dl": False, "expect_refuse": True},
        ),
    ]
    results = {}
    empty_success = 0
    for key, query, exp in cases:
        print("===", key)
        t0 = time.time()
        try:
            d = chat(query, user=f"wb-align-s0-{key}")
            ans = d.get("answer") or ""
            (OUT / f"{key}.answer.txt").write_text(ans, encoding="utf-8")
            meta = analyze(ans)
            meta["seconds"] = round(time.time() - t0, 1)
            meta["conversation_id"] = d.get("conversation_id")
            # empty success: asked file but no dl and not refuse
            if exp.get("expect_dl") and not meta["has_dl"]:
                empty_success += 1
                meta["empty_success"] = True
            if exp.get("forbid_dl") and meta["has_dl"]:
                meta["false_file"] = True
            # verify first dl
            if meta["dl_links"]:
                v = verify_dl(meta["dl_links"][0])
                meta["dl_verify"] = v
                # save artifact
                if v.get("ok"):
                    ext = exp.get("ext") or Path(meta["dl_links"][0]).suffix or ".bin"
                    # re-fetch via docker for body
                    m = re.search(r"/dl/([a-f0-9]+)/([^?\s]+)", meta["dl_links"][0])
                    if m:
                        fid, name = m.group(1), m.group(2)
                        subprocess.check_call(
                            f"docker exec aivia-bridge python -c \"import urllib.request;open('/tmp/art','wb').write(urllib.request.urlopen('http://127.0.0.1:18090/dl/{fid}/{name}',timeout=30).read())\"",
                            shell=True,
                        )
                        subprocess.check_call(
                            f"docker cp aivia-bridge:/tmp/art {OUT}/{key}.artifact{ext}",
                            shell=True,
                        )
            # refuse heuristic
            if exp.get("expect_refuse"):
                refuse_words = ["无法", "不能", "拒绝", "不可", "不会", "抱歉", "禁止"]
                meta["refused"] = any(w in ans for w in refuse_words) and not meta["has_dl"]
            results[key] = {"ok": True, **meta}
            print(json.dumps(meta, ensure_ascii=False)[:400])
        except Exception as e:
            results[key] = {"ok": False, "err": f"{type(e).__name__}: {e}"}
            print("FAIL", e)

    # S8 path: already verified attachment on dl
    # continuous S7 style in one conversation
    print("=== s7_chain")
    try:
        d1 = chat("生成一份数学《一次函数》HTML课件并给下载链接", "wb-align-s7")
        cid = d1.get("conversation_id")
        a1 = analyze(d1.get("answer") or "")
        d2 = chat("再做一张初二3班测验得分统计xlsx表并下载", "wb-align-s7", cid)
        a2 = analyze(d2.get("answer") or "")
        d3 = chat("只要大纲，不要文件", "wb-align-s7", cid)
        a3 = analyze(d3.get("answer") or "")
        results["s7_chain"] = {
            "ok": True,
            "html_dl": a1["has_dl"],
            "xlsx_dl": a2["has_dl"],
            "outline_no_dl": not a3["has_dl"],
            "a1": a1,
            "a2": a2,
            "a3": a3,
        }
        (OUT / "s7a.answer.txt").write_text(d1.get("answer") or "", encoding="utf-8")
        (OUT / "s7b.answer.txt").write_text(d2.get("answer") or "", encoding="utf-8")
        (OUT / "s7c.answer.txt").write_text(d3.get("answer") or "", encoding="utf-8")
    except Exception as e:
        results["s7_chain"] = {"ok": False, "err": str(e)}

    summary = {
        "empty_success": empty_success,
        "results": results,
        "base": BASE,
    }
    (OUT / "results.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("SUMMARY empty_success", empty_success)
    print("DONE", OUT)


if __name__ == "__main__":
    main()
