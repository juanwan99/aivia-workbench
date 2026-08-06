#!/usr/bin/env python3
"""Publish S2.1: PackDownload neutral defaults + system prompt. No secrets printed."""
from __future__ import annotations

import json
import re
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

APP_ID = "fc3e14da-2861-4009-a888-730a6b993011"
PACK_SRC = Path("/tmp/packdownload_s2.1.py")
SYS_SRC = Path("/tmp/general-wb-s2.1-system.txt")


def psql_t(sql: str) -> str:
    return subprocess.check_output(
        [
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
        ],
        text=True,
    ).strip()


def main() -> None:
    if not PACK_SRC.exists():
        raise SystemExit(f"missing {PACK_SRC}")
    if not SYS_SRC.exists():
        raise SystemExit(f"missing {SYS_SRC}")
    new_system = SYS_SRC.read_text(encoding="utf-8")
    pack_tpl = PACK_SRC.read_text(encoding="utf-8")

    src_wf = psql_t(f"select workflow_id from apps where id='{APP_ID}';")
    if not src_wf:
        raise SystemExit("no workflow_id")
    print("SRC_WF", src_wf)

    g = json.loads(psql_t(f"select graph from workflows where id='{src_wf}'"))
    features = json.loads(psql_t(f"select features from workflows where id='{src_wf}'"))

    # extract live token from current pack node
    dl_url, dl_tok = "http://aivia-bridge:18090/dl/put", ""
    for n in g["nodes"]:
        code = (n.get("data") or {}).get("code") or ""
        if "DL_PUT_TOKEN" in code or "DL_PUT" in code:
            m = re.search(r'DL_PUT_URL\s*=\s*"([^"]+)"', code)
            if m:
                dl_url = m.group(1)
            m = re.search(r'DL_PUT_TOKEN\s*=\s*"([^"]+)"', code)
            if m:
                dl_tok = m.group(1)
    if len(dl_tok) < 16:
        raise SystemExit("token missing/short")
    print("token_len", len(dl_tok), "dl_url", dl_url)

    pack_code = pack_tpl.replace("__DL_PUT_URL__", dl_url).replace(
        "__DL_PUT_TOKEN__", dl_tok
    )
    if "__DL_PUT" in pack_code:
        raise SystemExit("token inject failed")

    llm_n = pack_n = 0
    for n in g["nodes"]:
        d = n.setdefault("data", {})
        if d.get("type") == "llm":
            d["prompt_template"] = [{"role": "system", "text": new_system}]
            llm_n += 1
        if d.get("type") == "code" and (
            "DL_PUT" in (d.get("code") or "") or "PackDownload" in (d.get("title") or "")
        ):
            # prefer code nodes that upload
            if "DL_PUT" in (d.get("code") or "") or "content_b64" in (
                d.get("code") or ""
            ):
                d["code"] = pack_code
                pack_n += 1

    if llm_n < 1:
        raise SystemExit("no llm")
    if pack_n < 1:
        # broader match
        for n in g["nodes"]:
            d = n.setdefault("data", {})
            code = d.get("code") or ""
            if d.get("type") == "code" and (
                "build_docx" in code or "_pack(" in code or "DOWNLOAD_READY" in code
            ):
                d["code"] = pack_code
                pack_n += 1
    if pack_n < 1:
        raise SystemExit("no pack node")
    print("patched llm", llm_n, "pack", pack_n)

    # keep opening/suggested from current features
    graph_s = json.dumps(g, ensure_ascii=False)
    feat_s = json.dumps(features, ensure_ascii=False)
    new_id = str(uuid.uuid4())
    version = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
    tag = "g" + uuid.uuid4().hex
    tag2 = "f" + uuid.uuid4().hex
    sql = (
        "BEGIN;\n"
        "INSERT INTO workflows (\n"
        "  id, tenant_id, app_id, type, version, graph, features,\n"
        "  created_by, created_at, updated_by, updated_at, marked_name, marked_comment,\n"
        "  environment_variables, conversation_variables\n"
        ")\n"
        "SELECT\n"
        f"  '{new_id}', tenant_id, app_id, type, '{version}',\n"
        f"  ${tag}${graph_s}${tag}$::json,\n"
        f"  ${tag2}${feat_s}${tag2}$::json,\n"
        "  created_by, now(), updated_by, now(), 'general-wb-s2.1', 'S2.1-HOTFIX pack+prompt',\n"
        "  environment_variables, conversation_variables\n"
        f"FROM workflows WHERE id='{src_wf}';\n"
        f"UPDATE apps SET workflow_id='{new_id}', name='Aivia 通用 Agent', "
        f"updated_at=now() WHERE id='{APP_ID}';\n"
        "COMMIT;\n"
    )
    Path("/tmp/publish_s2_1.sql").write_text(sql, encoding="utf-8")
    with open("/tmp/publish_s2_1.sql", "rb") as f:
        subprocess.check_call(
            [
                "docker",
                "exec",
                "-i",
                "dify-db_postgres-1",
                "psql",
                "-U",
                "postgres",
                "-d",
                "dify",
            ],
            stdin=f,
        )
    subprocess.call(
        ["docker", "exec", "dify-redis-1", "redis-cli", "FLUSHDB"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    Path("/tmp/general-wb-s2.1-wf-id.txt").write_text(new_id, encoding="utf-8")
    print("NEW_WF", new_id)
    print(
        "APP",
        psql_t(f"select name||'|'||workflow_id from apps where id='{APP_ID}';"),
    )
    # verify defaults in live graph
    g2 = json.loads(psql_t(f"select graph from workflows where id='{new_id}'"))
    for n in g2["nodes"]:
        c = (n.get("data") or {}).get("code") or ""
        if "文档.docx" in c and "教案.docx" not in c.split("文档.docx")[0][-80:]:
            if 'else "文档.docx"' in c or 'else "文档.docx"' in c or 'else "文档.docx"' in c:
                pass
        if "DL_PUT" in c:
            print(
                "pack_defaults",
                "教案.docx" in c,
                "文档.docx" in c,
                "课件.html" in c,
                "页面.html" in c,
            )
            # count educational defaults as fallback only if still present as default
            bad = bool(
                re.search(r'else\s+"教案\.docx"', c)
                or re.search(r'else\s+"课件\.html"', c)
            )
            print("bad_edu_default", bad)
    for n in g2["nodes"]:
        d = n.get("data") or {}
        if d.get("type") == "llm":
            t = ""
            for p in d.get("prompt_template") or []:
                if p.get("role") == "system":
                    t = p.get("text") or ""
            print(
                "sys_has_3obs",
                "至少 3 条中性观察" in t or "中性观察" in t,
                "sys_len",
                len(t),
            )
    print("DONE")


if __name__ == "__main__":
    main()
