#!/usr/bin/env python3
"""Publish fixed workflow version with dollar-quoted JSON (safe)."""
from __future__ import annotations

import json
import re
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

# import NEW_SYSTEM and PACK_TEMPLATE pieces by reusing logic inline
import importlib.util

# load previous module if present
spec_path = Path("/tmp/_patch_workflow.py")
# We'll redefine essentials here to be self-contained

APP_ID = "fc3e14da-2861-4009-a888-730a6b993011"
SRC_WF = "898715d1-ddbd-4405-a883-9f566634a9fb"

NEW_SYSTEM = open("/tmp/new_system.txt", encoding="utf-8").read() if Path("/tmp/new_system.txt").exists() else ""


def sh(*args, input=None):
    return subprocess.check_output(list(args), input=input, text=True)


def psql_t(sql: str) -> str:
    return sh(
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
    ).strip()


def main():
    # Build patched graph using the first script's outputs if available
    # Prefer re-run patch assembly here by reading /tmp/new-graph.json if first script partially ran
    graph_path = Path("/tmp/new-graph.json")
    feat_path = Path("/tmp/new-features.json")
    if not graph_path.exists() or not feat_path.exists():
        raise SystemExit("missing /tmp/new-graph.json — run assembly first")

    new_id = str(uuid.uuid4())
    version = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
    graph = graph_path.read_text(encoding="utf-8")
    feat = feat_path.read_text(encoding="utf-8")
    # validate json
    json.loads(graph)
    json.loads(feat)

    tag = "wfjson" + uuid.uuid4().hex[:8]
    tag2 = "wffeat" + uuid.uuid4().hex[:8]
    sql = f"""
BEGIN;
INSERT INTO workflows (
  id, tenant_id, app_id, type, version, graph, features,
  created_by, created_at, updated_by, updated_at, marked_name, marked_comment,
  environment_variables, conversation_variables
)
SELECT
  '{new_id}', tenant_id, app_id, type, '{version}',
  ${tag}${graph}${tag}$::json,
  ${tag2}${feat}${tag2}$::json,
  created_by, now(), updated_by, now(), 'fix-deploy', 'WB-FIX-DEPLOY R1-R4',
  environment_variables, conversation_variables
FROM workflows WHERE id='{SRC_WF}';
COMMIT;
"""
    Path("/tmp/ins2.sql").write_text(sql, encoding="utf-8")
    with open("/tmp/ins2.sql", "rb") as f:
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
    print(
        sh(
            "docker",
            "exec",
            "dify-db_postgres-1",
            "psql",
            "-U",
            "postgres",
            "-d",
            "dify",
            "-c",
            f"select id, version, marked_name, length(graph::text) from workflows where id='{new_id}';",
        )
    )
    Path("/tmp/wb-fix-new-wf-id.txt").write_text(new_id, encoding="utf-8")
    print("NEW_WF", new_id)


if __name__ == "__main__":
    main()
