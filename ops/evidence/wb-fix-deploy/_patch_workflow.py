#!/usr/bin/env python3
"""Patch scene-full workflow: delivery list, DOCX harden, outline strict, file_upload.

Token stays only in workflow code on server (already injected); never print token.
"""
from __future__ import annotations

import json
import re
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

APP_ID = "fc3e14da-2861-4009-a888-730a6b993011"
SRC_WF = "898715d1-ddbd-4405-a883-9f566634a9fb"  # scene-full


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
    )


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
            "-c",
            sql,
        ],
        text=True,
    )


NEW_SYSTEM = r"""你是 Aivia 个人工作台助手（课件 / 教案 / 报表 · 多场景）。内容由模型生成；下载由下游 PackDownload 打成 HTTPS 文件。

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

# PackDownload body without hardcoding token: read from existing node code
PACK_TEMPLATE = r'''# PackDownload — HTTPS file URL primary (PHASE-WB-FIX-DEPLOY). Sandbox → aivia-bridge /dl/put.
import re
import base64
import io
import json
import zipfile
import xml.sax.saxutils as xu
import urllib.request
import urllib.error

# Injected — do not commit real tokens to git.
DL_PUT_URL = __DL_PUT_URL__
DL_PUT_TOKEN = __DL_PUT_TOKEN__
PUBLIC_HINT = "https://workbench.aivia.asia/dl/"


def _esc(s: str) -> str:
    return xu.escape(str(s) if s is not None else "")


def _safe_name(name: str, default: str, ext: str) -> str:
    name = name or default
    name = re.sub(r"[^\w\u4e00-\u9fff.\-]+", "_", name)[:80]
    if not name.lower().endswith(ext):
        name = name + ext
    return name


def _build_xlsx(headers, rows) -> bytes:
    headers = [str(h) for h in headers]
    norm_rows = []
    for r in rows:
        if isinstance(r, dict):
            norm_rows.append([str(r.get(h, "")) for h in headers])
        else:
            cells = list(r)
            if len(cells) < len(headers):
                cells += [""] * (len(headers) - len(cells))
            norm_rows.append([str(c) for c in cells[: len(headers)]])

    def col_letter(n: int) -> str:
        s = ""
        n += 1
        while n:
            n, rem = divmod(n - 1, 26)
            s = chr(65 + rem) + s
        return s

    sheet_rows = []
    cells_xml = []
    for i, h in enumerate(headers):
        ref = f"{col_letter(i)}1"
        cells_xml.append(f'<c r="{ref}" t="inlineStr"><is><t>{_esc(h)}</t></is></c>')
    sheet_rows.append(f'<row r="1">{"".join(cells_xml)}</row>')
    for ri, row in enumerate(norm_rows, start=2):
        cells_xml = []
        for i, val in enumerate(row):
            ref = f"{col_letter(i)}{ri}"
            cells_xml.append(
                f'<c r="{ref}" t="inlineStr"><is><t>{_esc(val)}</t></is></c>'
            )
        sheet_rows.append(f'<row r="{ri}">{"".join(cells_xml)}</row>')

    sheet1 = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(sheet_rows)}</sheetData></worksheet>'
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets></workbook>'
    )
    wb_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        'Target="worksheets/sheet1.xml"/>'
        "</Relationships>"
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        "</Types>"
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        "</Relationships>"
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        z.writestr("xl/worksheets/sheet1.xml", sheet1)
    return buf.getvalue()


def _build_docx_from_md(md: str) -> bytes:
    paras = []
    for line in (md or "").replace("\r\n", "\n").split("\n"):
        line = line.rstrip()
        if not line.strip():
            paras.append("<w:p/>")
            continue
        if line.startswith("#"):
            text = line.lstrip("#").strip()
            paras.append(
                "<w:p>"
                '<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
                f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{_esc(text)}</w:t></w:r>'
                "</w:p>"
            )
        else:
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", line)
            text = re.sub(r"`([^`]+)`", r"\1", text)
            paras.append(
                f'<w:p><w:r><w:t xml:space="preserve">{_esc(text)}</w:t></w:r></w:p>'
            )
    if not paras:
        paras = ["<w:p><w:r><w:t>empty</w:t></w:r></w:p>"]
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:body>{"".join(paras)}<w:sectPr/></w:body></w:document>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        "</Types>"
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="word/document.xml"/>'
        "</Relationships>"
    )
    doc_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>'
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
    return buf.getvalue()


def _parse_csv_block(block: str):
    lines = [ln for ln in block.strip().splitlines() if ln.strip()]
    if not lines:
        return None, None
    if "|" in lines[0]:
        rows = []
        for ln in lines:
            if re.match(r"^\s*\|?\s*:?-{2,}", ln):
                continue
            parts = [p.strip() for p in ln.strip().strip("|").split("|")]
            if parts:
                rows.append(parts)
        if len(rows) < 2:
            return None, None
        return rows[0], rows[1:]
    delim = "\t" if "\t" in lines[0] and lines[0].count("\t") >= lines[0].count(",") else ","
    rows = [[c.strip().strip('"') for c in ln.split(delim)] for ln in lines]
    if len(rows) < 2:
        return None, None
    return rows[0], rows[1:]


def _parse_table_json(block: str):
    try:
        data = json.loads(block)
    except Exception:
        return None, None
    if isinstance(data, dict):
        headers = data.get("headers") or data.get("columns") or []
        rows = data.get("rows") or data.get("data") or []
        if headers and rows:
            return [str(h) for h in headers], rows
    if isinstance(data, list) and data and isinstance(data[0], dict):
        headers = list(data[0].keys())
        rows = [[str(r.get(h, "")) for h in headers] for r in data]
        return headers, rows
    return None, None


def _upload(filename: str, mime: str, blob: bytes) -> dict:
    payload = {
        "filename": filename,
        "mime": mime,
        "content_b64": base64.b64encode(blob).decode("ascii"),
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        DL_PUT_URL,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Aivia-Dl-Put": DL_PUT_TOKEN,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")[:300]
        return {"ok": False, "error": f"upload HTTP {e.code}: {err}"}
    except Exception as e:
        return {"ok": False, "error": f"upload failed: {type(e).__name__}: {e}"}
    url = (body or {}).get("url") or ""
    if not url.startswith("https://"):
        return {"ok": False, "error": f"bad upload response url: {url!r}"}
    if "data:" in url:
        return {"ok": False, "error": "refusing data-URL as primary download path"}
    return {"ok": True, "url": url, "filename": body.get("filename") or filename}


def _pack(filename: str, mime: str, blob: bytes, preview: str) -> dict:
    up = _upload(filename, mime, blob)
    if not up.get("ok"):
        answer = (
            f"失败：未能生成可点击的 HTTPS 下载链接。\n"
            f"原因：{up.get('error')}\n"
            f"请稍后重试或联系管理员（下载落盘服务）。\n\n"
            f"<details><summary>内容预览（非下载）</summary>\n\n{preview}\n\n</details>"
        )
        return {
            "has_file": "no",
            "filename": "",
            "answer": answer,
            "download_marker": "NO_FILE",
        }
    url = up["url"]
    # R2: stable multi-line delivery list
    answer = (
        f"## 交付清单\n"
        f"| # | 文件名 | 类型 | 下载 |\n"
        f"|---|--------|------|------|\n"
        f"| 1 | {filename} | {mime.split(';')[0]} | [点击下载]({url}) |\n\n"
        f"DOWNLOAD_READY\n\n"
        f"- **文件名**：{filename}\n"
        f"- **HTTPS**：{url}\n"
        f"- **主路径**：https 文件 URL（非 data-URL）\n\n"
        f"[点击下载 {filename}]({url})\n\n"
        f"<details><summary>内容预览（备用）</summary>\n\n{preview}\n\n</details>"
    )
    return {
        "has_file": "yes",
        "filename": filename,
        "answer": answer,
        "download_marker": "DOWNLOAD_READY",
    }


def _is_outline_only(text: str) -> bool:
    t = text or ""
    if re.search(r"交付文件[：:]\s*\S+\.(html|docx|xlsx|md)\b", t, re.I):
        return False
    if re.search(r"```(?:html|csv|tsv|table)", t, re.I):
        return False
    # explicit outline / no-file cues
    if re.search(
        r"(只要大纲|不要文件|别下载|不要下载|列要点就行|列几点就行|先列提纲|严禁.*下载|不要生成任何下载)",
        t,
    ):
        return True
    if re.search(r"(大纲|要点|提纲)", t) and not re.search(
        r"(课件|教案|docx|xlsx|excel|html|下载|交付文件)", t, re.I
    ):
        return True
    return False


def _extract_md(text: str) -> str | None:
    m = re.search(r"```(?:markdown|md)\s*(.*?)```", text, re.S | re.I)
    if m:
        return m.group(1).strip()
    # plain text body if long enough and looks like lesson plan
    if re.search(r"(课题|教学目标|教学过程|作业)", text) and len(text) > 80:
        # strip delivery line
        body = re.sub(r"交付文件[：:].*", "", text)
        body = re.sub(r"```.*?```", "", body, flags=re.S)
        return body.strip() or None
    return None


def main(llm_text: str) -> dict:
    text = llm_text or ""

    # R4: outline-only hard skip packing
    if _is_outline_only(text):
        clean = text
        # strip accidental download markers if model slipped
        clean = re.sub(r"DOWNLOAD_READY\s*", "", clean)
        clean = re.sub(r"https://workbench\.aivia\.asia/dl/\S+", "", clean)
        return {
            "has_file": "no",
            "filename": "",
            "answer": clean.strip() or text,
            "download_marker": "NO_FILE",
        }

    # ---- XLSX ----
    want_xlsx = bool(
        re.search(r"交付文件[：:]\s*[^\s\n]+\.xlsx", text, re.I)
        or re.search(r"```(?:csv|tsv|table-json|table)", text, re.I)
        or re.search(r"\.xlsx", text, re.I)
    )
    if want_xlsx:
        headers, rows = None, None
        mjson = re.search(r"```table-json\s*(.*?)```", text, re.S | re.I)
        if mjson:
            headers, rows = _parse_table_json(mjson.group(1))
        if not headers:
            mcsv = re.search(r"```(?:csv|tsv|table)\s*(.*?)```", text, re.S | re.I)
            if mcsv:
                headers, rows = _parse_csv_block(mcsv.group(1))
        if not headers:
            mt = re.search(
                r"(\|[^\n]+\|\s*\n\|(?:\s*:?-{2,}:?\s*\|)+\s*\n(?:\|[^\n]+\|\s*\n?)+)",
                text,
            )
            if mt:
                headers, rows = _parse_csv_block(mt.group(1))
        if headers and rows and len(rows) >= 1:
            fm = re.search(r"交付文件[：:]\s*([^\s\n]+\.xlsx)", text, re.I)
            filename = _safe_name(fm.group(1) if fm else "报表.xlsx", "报表.xlsx", ".xlsx")
            blob = _build_xlsx(headers, rows)
            prev = (
                "| "
                + " | ".join(headers)
                + " |\n| "
                + " | ".join(["---"] * len(headers))
                + " |\n"
                + "\n".join(
                    "| " + " | ".join(str(c) for c in r) + " |" for r in rows[:20]
                )
            )
            return _pack(
                filename,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                blob,
                f"```markdown\n{prev}\n```",
            )

    # ---- DOCX (R3 harden: docx intent + md body, not only exact pair) ----
    fm_docx = re.search(r"交付文件[：:]\s*([^\s\n]+\.docx)", text, re.I)
    want_docx = bool(fm_docx) or bool(
        re.search(r"(教案|Word|DOCX|\.docx)", text, re.I)
    ) and not want_xlsx
    md = _extract_md(text)
    if want_docx and md and not re.search(r"```html", text, re.I):
        filename = _safe_name(
            fm_docx.group(1) if fm_docx else "教案.docx", "教案.docx", ".docx"
        )
        blob = _build_docx_from_md(md)
        return _pack(
            filename,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            blob,
            f"```markdown\n{md[:4000]}\n```",
        )

    # ---- HTML ----
    m = re.search(r"```html\s*(.*?)```", text, re.S | re.I)
    html = m.group(1).strip() if m else None
    if not html:
        m2 = re.search(r"(<!DOCTYPE html>.*?</html>)", text, re.S | re.I)
        if m2:
            html = m2.group(1).strip()
    if html:
        fm = re.search(r"交付文件[：:]\s*([^\s\n]+\.html)", text, re.I)
        filename = _safe_name(fm.group(1) if fm else "课件.html", "课件.html", ".html")
        return _pack(
            filename,
            "text/html; charset=utf-8",
            html.encode("utf-8"),
            f"```html\n{html[:2000]}\n```",
        )

    # ---- Markdown fallback only if NOT docx-intent ----
    md_block = re.search(r"```(?:markdown|md)\s*(.*?)```", text, re.S | re.I)
    if md_block and not want_docx:
        md = md_block.group(1).strip()
        fm = re.search(r"交付文件[：:]\s*([^\s\n]+\.(?:md|markdown))", text, re.I)
        filename = _safe_name(fm.group(1) if fm else "教案.md", "教案.md", ".md")
        return _pack(
            filename,
            "text/markdown; charset=utf-8",
            md.encode("utf-8"),
            f"```markdown\n{md[:4000]}\n```",
        )

    # docx intent but failed to pack
    if want_docx:
        return {
            "has_file": "no",
            "filename": "",
            "answer": (
                "失败：未能打包 Word（.docx）。请确保回答含 ```markdown 正文且写明「交付文件：xxx.docx」。\n\n"
                + text
            ),
            "download_marker": "NO_FILE",
        }

    return {
        "has_file": "no",
        "filename": "",
        "answer": text if text.strip() else "失败：未能生成可下载产物，请补充主题后重试。",
        "download_marker": "NO_FILE",
    }
'''


def main():
    raw = psql_t(f"select graph from workflows where id='{SRC_WF}'")
    g = json.loads(raw)
    features_raw = psql_t(f"select features from workflows where id='{SRC_WF}'")
    features = json.loads(features_raw) if features_raw.strip() else {}

    # extract existing token/url from code node
    dl_url = "http://aivia-bridge:18090/dl/put"
    dl_tok = ""
    for n in g["nodes"]:
        d = n.get("data") or {}
        code = d.get("code") or ""
        if "DL_PUT_TOKEN" in code:
            m = re.search(r'DL_PUT_URL\s*=\s*"([^"]+)"', code)
            if m:
                dl_url = m.group(1)
            m = re.search(r'DL_PUT_TOKEN\s*=\s*"([^"]+)"', code)
            if m:
                dl_tok = m.group(1)
            break
    assert dl_tok and len(dl_tok) > 16, "missing DL_PUT_TOKEN in existing node"
    print("token_len", len(dl_tok), "url", dl_url)

    pack_code = PACK_TEMPLATE.replace("__DL_PUT_URL__", json.dumps(dl_url)).replace(
        "__DL_PUT_TOKEN__", json.dumps(dl_tok)
    )
    # json.dumps already quotes; template expects raw assignment values
    pack_code = PACK_TEMPLATE.replace("__DL_PUT_URL__", f'"{dl_url}"').replace(
        "__DL_PUT_TOKEN__", f'"{dl_tok}"'
    )

    for n in g["nodes"]:
        d = n.get("data") or {}
        if d.get("type") == "llm":
            d["prompt_template"] = [{"role": "system", "text": NEW_SYSTEM}]
            # enable file vision/context if supported
            d["vision"] = d.get("vision") or {"enabled": False}
        if d.get("type") == "code" and (
            d.get("title") == "PackDownload" or "PackDownload" in (d.get("code") or "")[:80] or "DL_PUT" in (d.get("code") or "")
        ):
            d["code"] = pack_code
            print("patched PackDownload", len(pack_code))

    # R1 file upload features
    features["file_upload"] = {
        "enabled": True,
        "allowed_file_extensions": [".txt", ".md", ".csv", ".html", ".docx", ".pdf"],
        "allowed_file_types": ["document", "custom"],
        "allowed_file_upload_methods": ["local_file", "remote_url"],
        "number_limits": 3,
        "fileUploadConfig": {
            "file_size_limit": 5,
            "batch_count_limit": 3,
            "image_file_size_limit": 5,
        },
    }
    # keep opening / suggested
    features.setdefault(
        "opening_statement",
        "你好，我是 Aivia 个人工作台。可切换：HTML 课件、Word 教案、Excel 表、只要大纲。可上传材料再加工。要文件给 HTTPS /dl 下载。",
    )
    features["suggested_questions"] = [
        "请做一份初中生物「细胞结构」HTML 课件，要能下载",
        "写一份初中生物《细胞结构》一课时教案（Word 可下载）",
        "请做一份高一1班本周作业提交统计表，要能下载 Excel",
        "列要点就行：光合作用（不要文件）",
    ]

    new_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
    version = now
    tenant = psql_t(f"select tenant_id from workflows where id='{SRC_WF}'").strip()
    created_by = psql_t(f"select created_by from workflows where id='{SRC_WF}'").strip()
    graph_json = json.dumps(g, ensure_ascii=False)
    feat_json = json.dumps(features, ensure_ascii=False)
    # escape for SQL: use dollar quoting via file
    Path("/tmp/new-graph.json").write_text(graph_json, encoding="utf-8")
    Path("/tmp/new-features.json").write_text(feat_json, encoding="utf-8")
    Path("/tmp/insert_wf.sql").write_text(
        f"""
BEGIN;
INSERT INTO workflows (
  id, tenant_id, app_id, type, version, graph, features,
  created_by, created_at, updated_by, updated_at, marked_name, marked_comment,
  environment_variables, conversation_variables
)
SELECT
  '{new_id}', tenant_id, app_id, type, '{version}',
  pg_read_file('/tmp/new-graph.json')::json,
  pg_read_file('/tmp/new-features.json')::json,
  created_by, now(), updated_by, now(), 'fix-deploy', 'WB-FIX-DEPLOY R1-R4',
  environment_variables, conversation_variables
FROM workflows WHERE id='{SRC_WF}';
COMMIT;
""",
        encoding="utf-8",
    )
    # pg_read_file may not work inside container for host /tmp — copy into postgres container
    subprocess = __import__("subprocess")
    subprocess.check_call(
        ["docker", "cp", "/tmp/new-graph.json", "dify-db_postgres-1:/tmp/new-graph.json"]
    )
    subprocess.check_call(
        [
            "docker",
            "cp",
            "/tmp/new-features.json",
            "dify-db_postgres-1:/tmp/new-features.json",
        ]
    )
    # insert with python inside or psql variables
    insert_py = f"""
import json, subprocess, uuid
from datetime import datetime, timezone
graph=open('/tmp/new-graph.json',encoding='utf-8').read()
feat=open('/tmp/new-features.json',encoding='utf-8').read()
# escape single quotes for SQL
def esc(s):
    return s.replace("'", "''")
new_id='{new_id}'
version='{version}'
sql=f\"\"\"
INSERT INTO workflows (
  id, tenant_id, app_id, type, version, graph, features,
  created_by, created_at, updated_by, updated_at, marked_name, marked_comment,
  environment_variables, conversation_variables
)
SELECT
  '{{new_id}}', tenant_id, app_id, type, '{{version}}',
  '{{esc(graph)}}'::json,
  '{{esc(feat)}}'::json,
  created_by, now(), updated_by, now(), 'fix-deploy', 'WB-FIX-DEPLOY',
  environment_variables, conversation_variables
FROM workflows WHERE id='{SRC_WF}';
\"\"\"
open('/tmp/ins.sql','w',encoding='utf-8').write(sql)
print('sql_len', len(sql))
"""
    Path("/tmp/do_insert.py").write_text(insert_py, encoding="utf-8")
    subprocess.check_call(["python3", "/tmp/do_insert.py"])
    # run sql via docker exec -i
    with open("/tmp/ins.sql", "rb") as f:
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
    print(psql(f"select id, version, marked_name from workflows where app_id='{APP_ID}' order by created_at desc limit 3;"))
    print("NEW_WF", new_id)
    Path("/tmp/wb-fix-new-wf-id.txt").write_text(new_id, encoding="utf-8")


if __name__ == "__main__":
    main()
