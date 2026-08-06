#!/usr/bin/env python3
"""Dump workflow graph keys / prompt snippets for scene-full."""
import json
import subprocess
from pathlib import Path

APP = "fc3e14da-2861-4009-a888-730a6b993011"
WF = "898715d1-ddbd-4405-a883-9f566634a9fb"  # scene-full latest

def psql(sql: str) -> str:
    return subprocess.check_output(
        f'docker exec dify-db_postgres-1 psql -U postgres -d dify -tAc "{sql}"',
        shell=True,
        text=True,
    )

# columns of workflows
print("cols", subprocess.check_output(
    "docker exec dify-db_postgres-1 psql -U postgres -d dify -c \"select column_name from information_schema.columns where table_name='workflows' order by 1;\"",
    shell=True, text=True,
))

# export graph
graph = psql(f"select graph from workflows where id='{WF}';")
# may be huge - write to file
Path("/tmp/wf-graph.json").write_text(graph, encoding="utf-8")
print("graph_len", len(graph))
try:
    g = json.loads(graph)
except Exception as e:
    print("json fail", e, graph[:200])
    raise

nodes = g.get("nodes") or []
print("nodes", len(nodes))
for n in nodes:
    data = n.get("data") or {}
    ntype = data.get("type") or n.get("type")
    title = data.get("title") or data.get("name") or ""
    print("-", n.get("id"), ntype, title)
    # print prompt snippets
    for k in ("prompt_template", "instruction", "text", "code", "system_prompt", "pre_prompt"):
        v = data.get(k)
        if v:
            s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
            print("  ", k, "len", len(s), "head", s[:180].replace("\n"," "))

# features / file upload on app
print("=== features ===")
print(psql(f"select features from apps where id='{APP}';")[:500])
# draft workflow?
print("=== draft ===")
print(subprocess.check_output(
    f"docker exec dify-db_postgres-1 psql -U postgres -d dify -c \"select id, version, marked_name from workflows where app_id='{APP}' and version='draft';\"",
    shell=True, text=True,
))
