#!/usr/bin/env python3
"""Assemble patched scene-full workflow and publish as new version."""
from __future__ import annotations

import json
import re
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

APP_ID = "fc3e14da-2861-4009-a888-730a6b993011"
SRC_WF = "898715d1-ddbd-4405-a883-9f566634a9fb"

NEW_SYSTEM = """你是 Aivia 个人工作台助手（课件 / 教案 / 报表 · 多场景）。内容由模型生成；下载由下游 PackDownload 打成 HTTPS 文件。

【意图优先 · 防串台 · 每轮只干当前任务】
先判断用户本轮意图，只做一类，禁止把上一任务产物类型带到本轮：
- 课件/HTML → 仅 HTML
- 教案/Word/DOCX → 仅 DOCX（必须 ```markdown 正文 + 行「交付文件：xxx.docx」）
- 表/Excel/统计/登记 → 仅 XLSX（```csv + 交付文件：xxx.xlsx）
- 只要大纲 / 不要文件 / 别下载 / 「列要点就行」「列几点就行」「先列提纲」→ **仅文字大纲**；**严禁**「交付文件」、DOWNLOAD_READY、```html/```csv、任何下载链接
- 写成绩库/教务库/上传成功 → 人话拒绝，禁止假成功
- 改一版/加练习/加列 → 在同会话产出完整新文件（同类型）
- 用户附带文件/素材 → **基于素材再加工** 出对应格式产物

【强制纪律 · 空成功禁止】
1. 要文件：必须给出完整产物块 + 行「交付文件：文件名.扩展名」（扩展名仅 .html/.docx/.xlsx/.md）。
2. 禁止无产物说「已完成/成功」；做不到明确说失败与原因。
3. 信息不足最多澄清 1 次，否则合理默认并执行。
4. 同会话改稿：完整新文件，不要只 diff。
5. 禁止编造「已写入业务库 / 已上传成绩 / 已同步教务」。
6. 连续切换任务时：只响应最后一条用户意图。
7. Word/教案请求：**禁止**只交 md 而不写交付文件 .docx。

【HTML 课件】完整 ```html 单文件；交付文件：课件-<主题>.html
【教案 DOCX】完整 ```markdown；交付文件：教案-<主题>.docx；含课题、目标、重难点、过程、作业。
【Excel XLSX】```csv 表头+≥3行；交付文件：报表-<主题>.xlsx
【大纲 only】清晰要点列表；禁止交付文件行；禁止代码块出件。
【拒写库】说明不连接教务/成绩库；可改为导出 Excel 模板供人工导入。
【极短请求默认】课件→HTML；报表→xlsx；教案/Word→docx。
"""


def sh_out(args, input_bytes=None):
    return subprocess.check_output(args, input=input_bytes)


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


def load_pack_code(dl_url: str, dl_tok: str) -> str:
    # Read template from companion file written next to this script on server
    p = Path("/tmp/packdownload_fixed.py")
    if not p.exists():
        raise SystemExit("missing /tmp/packdownload_fixed.py")
    code = p.read_text(encoding="utf-8")
    code = code.replace("__DL_PUT_URL__", dl_url).replace("__DL_PUT_TOKEN__", dl_tok)
    return code


def main():
    raw = psql_t(f"select graph from workflows where id='{SRC_WF}'")
    g = json.loads(raw)
    features = json.loads(psql_t(f"select features from workflows where id='{SRC_WF}'"))

    dl_url, dl_tok = "http://aivia-bridge:18090/dl/put", ""
    for n in g["nodes"]:
        code = (n.get("data") or {}).get("code") or ""
        if "DL_PUT_TOKEN" in code:
            m = re.search(r'DL_PUT_URL\s*=\s*"([^"]+)"', code)
            if m:
                dl_url = m.group(1)
            m = re.search(r'DL_PUT_TOKEN\s*=\s*"([^"]+)"', code)
            if m:
                dl_tok = m.group(1)
    assert len(dl_tok) > 16
    print("token_len", len(dl_tok))

    pack_code = load_pack_code(dl_url, dl_tok)
    print("pack_code_len", len(pack_code))

    for n in g["nodes"]:
        d = n.setdefault("data", {})
        if d.get("type") == "llm":
            d["prompt_template"] = [{"role": "system", "text": NEW_SYSTEM}]
            print("llm patched")
        if d.get("type") == "code" and "DL_PUT" in (d.get("code") or ""):
            d["code"] = pack_code
            print("code patched")

    features["file_upload"] = {
        "enabled": True,
        "allowed_file_extensions": [".txt", ".md", ".csv", ".html", ".docx", ".pdf"],
        "allowed_file_types": ["document", "custom"],
        "allowed_file_upload_methods": ["local_file", "remote_url"],
        "number_limits": 3,
    }
    features["opening_statement"] = (
        "你好，我是 Aivia 个人工作台。可切换：HTML 课件、Word 教案、Excel 表、只要大纲。"
        "可上传材料再加工。要文件给 HTTPS /dl 下载（非 data-URL）。"
    )
    features["suggested_questions"] = [
        "请做一份初中生物「细胞结构」HTML 课件，要能下载",
        "写一份初中生物《细胞结构》一课时教案（Word 可下载）",
        "请做一份高一1班本周作业提交统计表，要能下载 Excel",
        "列要点就行：光合作用（不要文件）",
    ]

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
        "  created_by, now(), updated_by, now(), 'fix-deploy', 'WB-FIX-DEPLOY R1-R4',\n"
        "  environment_variables, conversation_variables\n"
        f"FROM workflows WHERE id='{SRC_WF}';\n"
        "COMMIT;\n"
    )
    Path("/tmp/publish_wf.sql").write_text(sql, encoding="utf-8")
    with open("/tmp/publish_wf.sql", "rb") as f:
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
        subprocess.check_output(
            [
                "docker",
                "exec",
                "dify-db_postgres-1",
                "psql",
                "-U",
                "postgres",
                "-d",
                "dify",
                "-c",
                f"select id, marked_name, left(version,19), length(graph::text) gl from workflows where id='{new_id}';",
            ],
            text=True,
        )
    )
    Path("/tmp/wb-fix-new-wf-id.txt").write_text(new_id, encoding="utf-8")
    print("NEW_WF", new_id)
    # Dify advanced-chat uses latest non-draft version automatically by created_at in many versions;
    # also check workflow_id on apps
    print("app cols sample:")
    print(
        subprocess.check_output(
            [
                "docker",
                "exec",
                "dify-db_postgres-1",
                "psql",
                "-U",
                "postgres",
                "-d",
                "dify",
                "-c",
                "select column_name from information_schema.columns where table_name='apps' and column_name like '%workflow%';",
            ],
            text=True,
        )
    )


if __name__ == "__main__":
    main()
