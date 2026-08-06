#!/usr/bin/env python3
"""Publish S4.1 pack + system prompt. No secrets printed."""
from __future__ import annotations

import json
import re
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

APP_ID = "fc3e14da-2861-4009-a888-730a6b993011"
PACK_SRC = Path("/tmp/packdownload_s4.1.py")
SYS_SRC = Path("/tmp/general-wb-s4.1-system.txt")


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
    if not PACK_SRC.exists() or not SYS_SRC.exists():
        raise SystemExit("missing pack or system")
    new_system = SYS_SRC.read_text(encoding="utf-8")
    pack_tpl = PACK_SRC.read_text(encoding="utf-8")
    if "_is_delivery_list_table" not in pack_tpl:
        raise SystemExit("s4.1 anti-nest missing")

    src_wf = psql_t(f"select workflow_id from apps where id='{APP_ID}';")
    print("SRC_WF", src_wf)
    g = json.loads(psql_t(f"select graph from workflows where id='{src_wf}';"))
    features = json.loads(psql_t(f"select features from workflows where id='{src_wf}'"))

    dl_url, dl_tok = "http://aivia-bridge:18090/dl/put", ""
    for n in g["nodes"]:
        code = (n.get("data") or {}).get("code") or ""
        if "DL_PUT" in code:
            m = re.search(r'DL_PUT_URL\s*=\s*"([^"]+)"', code)
            if m:
                dl_url = m.group(1)
            m = re.search(r'DL_PUT_TOKEN\s*=\s*"([^"]+)"', code)
            if m:
                dl_tok = m.group(1)
    if len(dl_tok) < 16:
        raise SystemExit("token short")
    print("token_len", len(dl_tok))

    pack_code = pack_tpl.replace("__DL_PUT_URL__", dl_url).replace(
        "__DL_PUT_TOKEN__", dl_tok
    )
    if "__DL_PUT" in pack_code:
        raise SystemExit("inject failed")

    llm_n = pack_n = 0
    for n in g["nodes"]:
        d = n.setdefault("data", {})
        if d.get("type") == "llm":
            d["prompt_template"] = [{"role": "system", "text": new_system}]
            llm_n += 1
        code = d.get("code") or ""
        if d.get("type") == "code" and (
            "DL_PUT" in code or "_pack(" in code or "DOWNLOAD_READY" in code
        ):
            d["code"] = pack_code
            pack_n += 1
    if llm_n < 1 or pack_n < 1:
        raise SystemExit(f"patch fail llm={llm_n} pack={pack_n}")
    print("patched llm", llm_n, "pack", pack_n)

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
        "  created_by, now(), updated_by, now(), 'general-wb-s4.1', 'S4.1 anti-nest pack+prompt',\n"
        "  environment_variables, conversation_variables\n"
        f"FROM workflows WHERE id='{src_wf}';\n"
        f"UPDATE apps SET workflow_id='{new_id}', name='Aivia 通用 Agent', "
        f"updated_at=now() WHERE id='{APP_ID}';\n"
        "COMMIT;\n"
    )
    Path("/tmp/publish_s4_1.sql").write_text(sql, encoding="utf-8")
    with open("/tmp/publish_s4_1.sql", "rb") as f:
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
    Path("/tmp/general-wb-s4.1-wf-id.txt").write_text(new_id, encoding="utf-8")
    print("NEW_WF", new_id)
    print("APP", psql_t(f"select name||'|'||workflow_id from apps where id='{APP_ID}';"))
    g2 = json.loads(psql_t(f"select graph from workflows where id='{new_id}'"))
    for n in g2["nodes"]:
        c = (n.get("data") or {}).get("code") or ""
        if "DL_PUT" in c:
            print(
                "pack",
                "_is_delivery_list_table" in c,
                "_pack_multi" in c,
                'else "教案.docx"' in c,
            )


if __name__ == "__main__":
    main()
