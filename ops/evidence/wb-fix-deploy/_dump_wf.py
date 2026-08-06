#!/usr/bin/env python3
import json, subprocess
from pathlib import Path
WF = "898715d1-ddbd-4405-a883-9f566634a9fb"
graph = subprocess.check_output(
    f"docker exec dify-db_postgres-1 psql -U postgres -d dify -tAc \"select graph from workflows where id='{WF}';\"",
    shell=True, text=True,
)
g = json.loads(graph)
Path("/tmp/wf-scene-full.json").write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
for n in g["nodes"]:
    d = n.get("data") or {}
    if d.get("type") == "llm":
        Path("/tmp/wf-llm-prompt.json").write_text(json.dumps(d.get("prompt_template"), ensure_ascii=False, indent=2), encoding="utf-8")
        print("LLM prompt written")
    if d.get("type") == "code" or d.get("title") == "PackDownload":
        Path("/tmp/wf-packdownload.py").write_text(d.get("code") or "", encoding="utf-8")
        print("PackDownload code len", len(d.get("code") or ""))
        print("outputs", d.get("outputs"))
        print("variables", d.get("variables"))
    if d.get("type") == "start":
        Path("/tmp/wf-start.json").write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        print("start variables", d.get("variables"))
print("features in graph?", "features" in g)
if "features" in g:
    Path("/tmp/wf-features.json").write_text(json.dumps(g["features"], ensure_ascii=False, indent=2), encoding="utf-8")
# workflow features column
feat = subprocess.check_output(
    f"docker exec dify-db_postgres-1 psql -U postgres -d dify -tAc \"select features from workflows where id='{WF}';\"",
    shell=True, text=True,
)
Path("/tmp/wf-features-col.json").write_text(feat, encoding="utf-8")
print("features_col_len", len(feat))
print(feat[:800])
