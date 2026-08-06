#!/usr/bin/env python3
"""Publish general-agent S1 workflow: system prompt + opening + ≥6 suggested Qs.

Does NOT change PackDownload code (reuse live token). No secrets printed.
"""
from __future__ import annotations

import json
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

APP_ID = "fc3e14da-2861-4009-a888-730a6b993011"

NEW_SYSTEM = """你是 Aivia 通用 Agent（办公文档 / 表格 / 公众号文案 / 代码说明 / 分析摘要 / 改稿润色）。
内容由模型生成；需要可下载文件时，由下游 PackDownload 打成 HTTPS `/dl` 链接。

【定位】
- 默认入口 = 通用生产力助手，不是「仅教研 / 课件专员」。
- 教育场景仍可做，但只是能力之一，不写进主叙事。
- 做得到就交付；做不到明确失败原因。禁止空成功。

【意图优先 · 每轮只干当前任务】
先判断本轮意图，只做一类：
- Word/DOCX/公文/纪要/方案/通知/合同草稿 → 仅 DOCX（```markdown 正文 + 行「交付文件：xxx.docx」）
- Excel/表格/台账/统计/清单/CSV → 仅 XLSX（```csv + 行「交付文件：xxx.xlsx」）
- HTML/单页说明页/简单页面 → 仅 HTML（```html + 交付文件：xxx.html）
- 公众号/推文/社媒文案/营销短文 → 默认正文（要文件才出 docx）
- 代码解释/小片段/伪代码/排错思路 → 文字+代码块；不要硬塞下载
- 分析/摘要/对比/要点 → 文字；要表才出 xlsx
- 改稿/润色/扩写/缩写 → 在同会话产出完整新版本（同类型）
- 只要短答 / 只要大纲 / 不要文件 / 列要点就行 → **仅文字**；**严禁**「交付文件」、DOWNLOAD_READY、假下载链接
- 写业务库/成绩库/教务库/「已上传成功」→ 人话拒绝，禁止假成功

【强制纪律 · 空成功禁止】
1. 要文件：必须完整产物块 + 行「交付文件：文件名.扩展名」（.html/.docx/.xlsx/.md）。
2. 禁止无产物说「已完成/成功」；做不到明确说失败与原因。
3. 信息不足最多澄清 1 次，否则合理默认并执行。
4. 同会话改稿：完整新文件/新正文，不要只 diff。
5. 禁止编造「已写入业务库 / 已同步 / 已推送后台」。
6. 连续切换任务时：只响应最后一条用户意图。
7. 短答路径：禁止出现 DOWNLOAD、/dl/、交付文件 行。

【DOCX】
- 完整 ```markdown；交付文件：文档-<主题>.docx
- 含标题、目的/背景、正文结构、结论或下一步（按场景裁剪）。

【XLSX】
- ```csv 表头 + ≥3 行真实感数据；交付文件：表格-<主题>.xlsx

【HTML】
- 完整 ```html 单文件；交付文件：页面-<主题>.html

【短答 / 大纲 only】
- 清晰要点或直接答案；禁止交付文件行；禁止用代码块伪装下载。

【拒写库】
- 说明本工作台不直连业务/教务库；可改为导出 Excel/Word 模板供人工导入。

【极短请求默认】
- 「Word/文档」→ 工作周报模板 docx
- 「Excel/表」→ 本周任务进度表 xlsx
- 「公号」→ 800 字内推文正文（不要文件）
- 「短答」→ 只答一句/几点，不要文件
"""

OPENING = (
    "你好，我是 Aivia 通用 Agent。"
    "可帮你：办公 Word、Excel 表、公众号文案、代码说明、分析摘要、改稿润色。"
    "要文件会给 HTTPS /dl 下载链接；只要短答不会硬塞文件；做不到会明确说失败。"
)

SUGGESTED = [
    "写一份本周工作周报（Word 可下载）",
    "做一张本周任务进度表，要能下载 Excel",
    "写一篇公众号推文：远程办公的 5 个效率习惯（不要文件）",
    "解释这段思路：用字典计数统计词频，给 Python 示例",
    "把下面要点扩写成邮件正文：延期一周、原因供应链、新交期下周五",
    "只要短答：1+1 等于几？（不要文件）",
    "改稿：把『大家好我今天想说一下项目进度其实还行』润色成正式周会发言",
    "做一份会议纪要模板（Word 可下载）：议题/决议/待办",
]


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
    src_wf = psql_t(f"select workflow_id from apps where id='{APP_ID}';")
    if not src_wf:
        raise SystemExit("no workflow_id on app")
    print("SRC_WF", src_wf)

    g = json.loads(psql_t(f"select graph from workflows where id='{src_wf}'"))
    features = json.loads(psql_t(f"select features from workflows where id='{src_wf}'"))

    llm_n = pack_n = 0
    for n in g["nodes"]:
        d = n.setdefault("data", {})
        if d.get("type") == "llm":
            d["prompt_template"] = [{"role": "system", "text": NEW_SYSTEM}]
            llm_n += 1
        # keep PackDownload code intact (token live)

    if llm_n < 1:
        raise SystemExit("no llm node")

    features["opening_statement"] = OPENING
    features["suggested_questions"] = SUGGESTED
    # keep file_upload if present; ensure not forced off
    if not isinstance(features.get("file_upload"), dict):
        features["file_upload"] = {
            "enabled": True,
            "allowed_file_extensions": [".txt", ".md", ".csv", ".html", ".docx", ".pdf"],
            "allowed_file_types": ["document", "custom"],
            "allowed_file_upload_methods": ["local_file", "remote_url"],
            "number_limits": 3,
        }

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
        "  created_by, now(), updated_by, now(), 'general-wb-s1', 'S1-GENERAL-WB W0 general agent',\n"
        "  environment_variables, conversation_variables\n"
        f"FROM workflows WHERE id='{src_wf}';\n"
        f"UPDATE apps SET workflow_id='{new_id}', name='Aivia 通用 Agent', "
        f"updated_at=now() WHERE id='{APP_ID}';\n"
        "COMMIT;\n"
    )
    sql_path = Path("/tmp/publish_general_s1.sql")
    sql_path.write_text(sql, encoding="utf-8")
    with open(sql_path, "rb") as f:
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
    # flush redis cache
    subprocess.call(
        ["docker", "exec", "dify-redis-1", "redis-cli", "FLUSHDB"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    Path("/tmp/general-wb-s1-wf-id.txt").write_text(new_id, encoding="utf-8")
    print("NEW_WF", new_id)
    print(
        "APP_NOW",
        psql_t(
            f"select id||'|'||name||'|'||workflow_id from apps where id='{APP_ID}';"
        ),
    )
    print(
        "MARKED",
        psql_t(
            f"select marked_name||'|'||left(version,19) from workflows where id='{new_id}';"
        ),
    )
    # dump features snapshot for evidence (no secrets)
    Path("/tmp/general-wb-s1-features.json").write_text(
        json.dumps(
            {
                "opening_statement": features["opening_statement"],
                "suggested_questions": features["suggested_questions"],
                "file_upload": features.get("file_upload"),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    Path("/tmp/general-wb-s1-system.txt").write_text(NEW_SYSTEM, encoding="utf-8")
    print("SNAPSHOT /tmp/general-wb-s1-features.json /tmp/general-wb-s1-system.txt")
    print("DONE pack_n=", pack_n, "llm_n=", llm_n)


if __name__ == "__main__":
    main()
