#!/usr/bin/env python3
"""Inspect live Dify app workflow (general-wb S1). No secrets printed."""
from __future__ import annotations

import json
import subprocess
import sys

APP_ID = "fc3e14da-2861-4009-a888-730a6b993011"


def psql(sql: str) -> str:
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
    row = psql(
        f"select id||'|'||coalesce(name,'')||'|'||coalesce(workflow_id::text,'') from apps where id='{APP_ID}';"
    )
    print("APP", row)
    wf = row.split("|")[-1] if row else ""
    if not wf:
        sys.exit("no workflow_id")
    print("WF", wf)
    print(
        "RECENT",
        psql(
            f"select string_agg(id||':'||coalesce(marked_name,'')||':'||left(version,19), E'\\n' order by created_at desc) from (select id,marked_name,version,created_at from workflows where app_id='{APP_ID}' order by created_at desc nulls last limit 5) t;"
        ),
    )
    features = json.loads(psql(f"select features::text from workflows where id='{wf}';"))
    print(
        "FEATURES",
        json.dumps(
            {
                "opening_statement": features.get("opening_statement"),
                "suggested_questions": features.get("suggested_questions"),
                "file_upload": features.get("file_upload"),
            },
            ensure_ascii=False,
            indent=2,
        ),
    )
    graph = json.loads(psql(f"select graph::text from workflows where id='{wf}';"))
    for n in graph.get("nodes", []):
        d = n.get("data") or {}
        if d.get("type") == "llm":
            for p in d.get("prompt_template") or []:
                if p.get("role") == "system":
                    t = p.get("text") or ""
                    print("SYSTEM_HEAD")
                    print(t[:1500])
                    print("SYSTEM_LEN", len(t))
        code = d.get("code") or ""
        if "PUBLIC_HINT" in code or "DL_PUT" in code:
            print("PACK_LINES")
            for line in code.splitlines():
                if any(
                    k in line
                    for k in (
                        "PUBLIC",
                        "DL_PUT_URL",
                        "asyncova",
                        "workbench",
                        "DL_PUT_TOKEN",
                    )
                ):
                    if "TOKEN" in line:
                        print("  DL_PUT_TOKEN=<redacted len=%d>" % (len(line),))
                    else:
                        print(" ", line)


if __name__ == "__main__":
    main()
