# Aivia PackDownload · GENERAL-WB S4.1 (multi + anti nested delivery-sheet)
# Defaults: 文档.docx / 报表.xlsx / 页面.html / 文档.md
# NEVER default to 教案/课件 filenames.
# S4 multi docx+xlsx; S4.1 NEVER pack 交付清单 markdown as business xlsx.
# Deploy: replace Dify PackDownload code node with this file body.
# Source lineage: packdownload_s4.py

# PackDownload — HTTPS file URL primary (PHASE-DL-FIX). Sandbox → aivia-bridge /dl/put.
import re
import base64
import io
import json
import zipfile
import xml.sax.saxutils as xu
import urllib.request
import urllib.error

# Injected at deploy time from ECS secrets — do not commit real tokens to git.
DL_PUT_URL = "__DL_PUT_URL__"
DL_PUT_TOKEN = "__DL_PUT_TOKEN__"
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



def _is_delivery_list_table(headers, rows) -> bool:
    """True if table is a 交付清单 (meta), not business data — S4.1 anti-nest."""
    hs = [str(h) for h in (headers or [])]
    hjoin = " ".join(hs)
    meta_hits = sum(1 for k in ("文件名", "类型", "下载", "#") if k in hjoin or k in hs)
    if meta_hits >= 2 and ("文件名" in hjoin or "下载" in hjoin):
        return True
    blob = hjoin + " " + " ".join(str(c) for r in (rows or [])[:30] for c in r)
    has_dl = ("/dl/" in blob) or ("DOWNLOAD" in blob) or ("点击下载" in blob)
    has_meta = ("文件名" in blob and ("类型" in blob or "下载" in blob))
    has_biz = any(
        k in blob
        for k in (
            "单价",
            "月销量",
            "销量",
            "市占率",
            "市占",
            "营收",
            "产品A",
            "产品B",
            "产品C",
            "负责人",
            "状态",
            "任务",
        )
    )
    if has_meta and has_dl and not has_biz:
        return True
    if has_meta and not has_biz and meta_hits >= 2:
        return True
    return False


def _strip_prior_delivery_chrome(text: str) -> str:
    """Remove prior 交付清单 blocks so nested tables are not re-parsed as data."""
    t = text or ""
    t = re.sub(
        r"##\s*交付清单[\s\S]*?(?=```|交付文件[：:]|##\s|\Z)",
        "\n",
        t,
    )
    t = re.sub(r"DOWNLOAD_READY\s*", "", t)

    def _drop_meta_table(m):
        block = m.group(0)
        if "文件名" in block and ("下载" in block or "类型" in block):
            return "\n"
        return block

    t = re.sub(
        r"(\|[^\n]+\|\s*\n\|(?:\s*:?-{2,}:?\s*\|)+\s*\n(?:\|[^\n]+\|\s*\n?)+)",
        _drop_meta_table,
        t,
    )
    t = re.sub(r"(?m)^\s*https?://\S+/dl/\S+\s*$", "", t)
    return t


def _accept_xlsx(headers, rows):
    if not headers or not rows or len(rows) < 1:
        return None, None
    if _is_delivery_list_table(headers, rows):
        return None, None
    return headers, rows

def _upload(filename: str, mime: str, blob: bytes) -> dict:
    """Primary path: HTTPS file URL via bridge. Fail hard (no data-URL green)."""
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


def _extract_prose(text: str) -> str:
    """Keep LLM observations/conclusions outside code fences (S2.1 G7)."""
    t = text or ""
    t = re.sub(r"```.*?```", "\n", t, flags=re.S)
    t = re.sub(r"交付文件[：:].*", "", t)
    t = re.sub(r"DOWNLOAD_READY\s*", "", t)
    t = re.sub(r"https?://\S+/dl/\S+", "", t)
    # drop pure markdown tables
    t = re.sub(r"(?m)^\s*\|.*\|\s*$", "", t)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t[:4000] if t else ""


def _pack(filename: str, mime: str, blob: bytes, preview: str, prose: str = "") -> dict:
    up = _upload(filename, mime, blob)
    if not up.get("ok"):
        # Honest failure — do NOT fall back to data-URL for green CLAIM
        prefix = (prose.strip() + "\n\n") if (prose or "").strip() else ""
        answer = (
            f"{prefix}"
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
    prefix = (prose.strip() + "\n\n") if (prose or "").strip() else ""
    answer = (
        f"{prefix}"
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


def _pack_multi(items: list, prose: str = "") -> dict:
    """Pack multiple files (S4). items: filename/mime/blob/preview dicts."""
    if not items:
        return {
            "has_file": "no",
            "filename": "",
            "answer": "失败：无产物可打包。",
            "download_marker": "NO_FILE",
        }
    rows = []
    bullets = []
    links = []
    previews = []
    names = []
    for i, it in enumerate(items, 1):
        filename = it["filename"]
        mime = it["mime"]
        blob = it["blob"]
        preview = it.get("preview") or ""
        up = _upload(filename, mime, blob)
        if not up.get("ok"):
            prefix = (prose.strip() + "\n\n") if (prose or "").strip() else ""
            answer = (
                f"{prefix}"
                f"失败：未能生成可点击的 HTTPS 下载链接（第 {i} 个文件 {filename}）。\n"
                f"原因：{up.get('error')}\n"
                f"请稍后重试或联系管理员（下载落盘服务）。\n"
            )
            return {
                "has_file": "no",
                "filename": "",
                "answer": answer,
                "download_marker": "NO_FILE",
            }
        url = up["url"]
        names.append(filename)
        rows.append(
            f"| {i} | {filename} | {mime.split(';')[0]} | [点击下载]({url}) |"
        )
        bullets.append(f"- **文件名**：{filename}\n- **HTTPS**：{url}")
        links.append(f"[点击下载 {filename}]({url})")
        if preview:
            previews.append(f"### {filename}\n\n{preview}")
    prefix = (prose.strip() + "\n\n") if (prose or "").strip() else ""
    answer = (
        f"{prefix}"
        f"## 交付清单\n"
        f"| # | 文件名 | 类型 | 下载 |\n"
        f"|---|--------|------|------|\n"
        + "\n".join(rows)
        + "\n\nDOWNLOAD_READY\n\n"
        + "\n".join(bullets)
        + "\n- **主路径**：https 文件 URL（非 data-URL）\n\n"
        + "\n".join(links)
        + "\n\n<details><summary>内容预览（备用）</summary>\n\n"
        + "\n\n".join(previews)
        + "\n\n</details>"
    )
    return {
        "has_file": "yes",
        "filename": "+".join(names),
        "answer": answer,
        "download_marker": "DOWNLOAD_READY",
    }


def _is_outline_only(text: str) -> bool:
    t = text or ""
    if re.search(r"交付文件[：:]\s*\S+\.(html|docx|xlsx|md)\b", t, re.I):
        return False
    if re.search(r"```(?:html|csv|tsv|table)", t, re.I):
        return False
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


def _extract_md(text: str):
    m = re.search(r"```(?:markdown|md)\s*(.*?)```", text, re.S | re.I)
    if m:
        return m.group(1).strip()
    # S4: plain long structure + 交付文件 docx (model may omit fence)
    if re.search(r"交付文件[：:]\s*\S+\.docx", text, re.I) and len(text) > 200:
        body = re.sub(r"交付文件[：:].*", "", text)
        body = re.sub(r"```.*?```", "", body, flags=re.S)
        body = re.sub(r"DOWNLOAD_READY\s*", "", body)
        body = re.sub(r"https?://\S+/dl/\S+", "", body)
        body = body.strip()
        if len(body) > 120:
            return body
    if re.search(r"(课题|教学目标|教学过程|作业)", text) and len(text) > 80:
        body = re.sub(r"交付文件[：:].*", "", text)
        body = re.sub(r"```.*?```", "", body, flags=re.S)
        return body.strip() or None
    return None


def main(llm_text: str) -> dict:
    text = llm_text or ""

    # R4: outline-only hard skip packing
    if _is_outline_only(text):
        clean = re.sub(r"DOWNLOAD_READY\s*", "", text)
        clean = re.sub(r"https://workbench\.aivia\.asia/dl/\S+", "", clean)
        return {
            "has_file": "no",
            "filename": "",
            "answer": clean.strip() or text,
            "download_marker": "NO_FILE",
        }

    prose = _extract_prose(text)

    # ---- XLSX candidate (S4.1: strip delivery chrome; reject nested list tables) ----
    text_x = _strip_prior_delivery_chrome(text)
    want_xlsx = bool(
        re.search(r"交付文件[：:]\s*[^\s\n]+\.xlsx", text, re.I)
        or re.search(r"```(?:csv|tsv|table-json|table)", text_x, re.I)
        or re.search(r"\.xlsx", text, re.I)
    )
    xlsx_item = None
    xlsx_rejected_nested = False
    if want_xlsx:
        headers, rows = None, None
        mjson = re.search(r"```table-json\s*(.*?)```", text_x, re.S | re.I)
        if mjson:
            h0, r0 = _parse_table_json(mjson.group(1))
            if _is_delivery_list_table(h0, r0):
                xlsx_rejected_nested = True
            else:
                headers, rows = h0, r0
        if not headers:
            mcsv = re.search(r"```(?:csv|tsv|table)\s*(.*?)```", text_x, re.S | re.I)
            if mcsv:
                h0, r0 = _parse_csv_block(mcsv.group(1))
                if _is_delivery_list_table(h0, r0):
                    xlsx_rejected_nested = True
                else:
                    headers, rows = h0, r0
        if not headers:
            for mt in re.finditer(
                r"(\|[^\n]+\|\s*\n\|(?:\s*:?-{2,}:?\s*\|)+\s*\n(?:\|[^\n]+\|\s*\n?)+)",
                text_x,
            ):
                h0, r0 = _parse_csv_block(mt.group(1))
                if _is_delivery_list_table(h0, r0):
                    xlsx_rejected_nested = True
                    continue
                headers, rows = h0, r0
                break
        if headers and rows and len(rows) >= 1:
            names = re.findall(r"交付文件[：:]\s*([^\s\n]+\.xlsx)", text, re.I)
            raw_name = names[-1] if names else "报表.xlsx"
            filename = _safe_name(raw_name, "报表.xlsx", ".xlsx")
            blob = _build_xlsx(headers, rows)
            prev = (
                "| "
                + " | ".join(str(h) for h in headers)
                + " |\n| "
                + " | ".join(["---"] * len(headers))
                + " |\n"
                + "\n".join(
                    "| " + " | ".join(str(c) for c in r) + " |" for r in rows[:20]
                )
            )
            xlsx_item = {
                "filename": filename,
                "mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "blob": blob,
                "preview": f"```markdown\n{prev}\n```",
            }

    # ---- DOCX candidate ----
    fm_docx = re.search(r"交付文件[：:]\s*([^\s\n]+\.docx)", text, re.I)
    want_docx = bool(fm_docx) or (
        bool(re.search(r"(教案|Word|DOCX|\.docx)", text, re.I)) and not want_xlsx
    )
    # For multi intent, allow docx even if xlsx wanted
    multi_intent = bool(
        re.search(r"交付文件[：:]\s*[^\s\n]+\.docx", text, re.I)
        and re.search(r"交付文件[：:]\s*[^\s\n]+\.xlsx", text, re.I)
    )
    if multi_intent:
        want_docx = True
    md = _extract_md(text)
    docx_item = None
    if want_docx and md and not re.search(r"```html", text, re.I):
        filename = _safe_name(
            fm_docx.group(1) if fm_docx else "文档.docx", "文档.docx", ".docx"
        )
        blob = _build_docx_from_md(md)
        docx_item = {
            "filename": filename,
            "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "blob": blob,
            "preview": f"```markdown\n{md[:4000]}\n```",
        }

    if multi_intent and docx_item and xlsx_item:
        return _pack_multi([docx_item, xlsx_item], prose=prose)

    if multi_intent:
        got = [x for x in (docx_item, xlsx_item) if x]
        if len(got) == 1:
            it = got[0]
            return _pack(
                it["filename"],
                it["mime"],
                it["blob"],
                it["preview"],
                prose=prose if it is xlsx_item else "",
            )
        if not got:
            return {
                "has_file": "no",
                "filename": "",
                "answer": "失败：请求了 Word+Excel 双交付，但未能从回复中解析出完整产物块。请重试并确保含 ```markdown 与 ```csv。",
                "download_marker": "NO_FILE",
            }

    if xlsx_item:
        return _pack(
            xlsx_item["filename"],
            xlsx_item["mime"],
            xlsx_item["blob"],
            xlsx_item["preview"],
            prose=prose,
        )
    if docx_item:
        return _pack(
            docx_item["filename"],
            docx_item["mime"],
            docx_item["blob"],
            docx_item["preview"],
            prose="",
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
        filename = _safe_name(fm.group(1) if fm else "页面.html", "页面.html", ".html")
        return _pack(
            filename,
            "text/html; charset=utf-8",
            html.encode("utf-8"),
            f"```html\n{html[:2000]}\n```",
            prose=prose,
        )

    # S4.1: explicit xlsx ask but only nested 交付清单 / no business csv
    # Must run BEFORE markdown fallback (else 清单 fence becomes 文档.md).
    if re.search(r"交付文件[：:]\s*[^\s\n]+\.xlsx", text, re.I) and not xlsx_item:
        return {
            "has_file": "no",
            "filename": "",
            "answer": (
                "失败：未能从回复中解析出业务表格数据（csv）。\n"
                "请不要把「交付清单」当作表格内容；请输出 ```csv 表头+数据行，"
                "并写 交付文件：表格-<主题>.xlsx。"
            ),
            "download_marker": "NO_FILE",
        }

    # ---- Markdown fallback ----
    md_block = re.search(r"```(?:markdown|md)\s*(.*?)```", text, re.S | re.I)
    if md_block and not want_docx:
        md = md_block.group(1).strip()
        # refuse packing 交付清单 as .md
        if "文件名" in md and ("下载" in md or "/dl/" in md) and "单价" not in md:
            md = ""
        if md:
            fm = re.search(r"交付文件[：:]\s*([^\s\n]+\.(?:md|markdown))", text, re.I)
            # only pack md when user asked for .md
            if fm:
                filename = _safe_name(fm.group(1), "文档.md", ".md")
                return _pack(
                    filename,
                    "text/markdown; charset=utf-8",
                    md.encode("utf-8"),
                    f"```markdown\n{md[:4000]}\n```",
                    prose=prose,
                )

    return {
        "has_file": "no",
        "filename": "",
        "answer": text if text.strip() else "失败：未能生成可下载产物，请补充主题后重试。",
        "download_marker": "NO_FILE",
    }
