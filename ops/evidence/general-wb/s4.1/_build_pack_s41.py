#!/usr/bin/env python3
"""Build packdownload_s4.1.py from s4 with anti-nested-delivery-sheet fixes."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # aivia-workbench
# file is ops/evidence/general-wb/s4.1/_build -> parents[0]=s4.1 [1]=general-wb [2]=evidence [3]=ops [4]=root
ROOT = Path(__file__).resolve().parents[4]
src = (ROOT / "ops/evidence/general-wb/s4/packdownload_s4.py").read_text(encoding="utf-8")

src = src.replace(
    "# Aivia PackDownload · GENERAL-WB S4 (multi-deliverable)\n"
    "# Defaults: 文档.docx / 报表.xlsx / 页面.html / 文档.md\n"
    "# NEVER default to 教案/课件 filenames (education skin debt).\n"
    "# S4: BOTH docx+xlsx deliver lines -> pack two /dl links.\n"
    "# Deploy: replace Dify workflow PackDownload code node with this file body.\n"
    "# Source lineage: packdownload_s2.1.py\n",
    "# Aivia PackDownload · GENERAL-WB S4.1 (multi + anti nested delivery-sheet)\n"
    "# Defaults: 文档.docx / 报表.xlsx / 页面.html / 文档.md\n"
    "# NEVER default to 教案/课件 filenames.\n"
    "# S4 multi docx+xlsx; S4.1 NEVER pack 交付清单 markdown as business xlsx.\n"
    "# Deploy: replace Dify PackDownload code node with this file body.\n"
    "# Source lineage: packdownload_s4.py\n",
)

helper = r'''
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

'''

idx = src.find("def _upload(")
if idx < 0:
    raise SystemExit("no _upload")
src = src[:idx] + helper + src[idx:]

old = """    # ---- XLSX candidate ----
    want_xlsx = bool(
        re.search(r\"交付文件[：:]\\s*[^\\s\\n]+\\.xlsx\", text, re.I)
        or re.search(r\"```(?:csv|tsv|table-json|table)\", text, re.I)
        or re.search(r\"\\.xlsx\", text, re.I)
    )
    xlsx_item = None
    if want_xlsx:
        headers, rows = None, None
        mjson = re.search(r\"```table-json\\s*(.*?)```\", text, re.S | re.I)
        if mjson:
            headers, rows = _parse_table_json(mjson.group(1))
        if not headers:
            mcsv = re.search(r\"```(?:csv|tsv|table)\\s*(.*?)```\", text, re.S | re.I)
            if mcsv:
                headers, rows = _parse_csv_block(mcsv.group(1))
        if not headers:
            mt = re.search(
                r\"(\\|[^\\n]+\\|\\s*\\n\\|(?:\\s*:?-{2,}:?\\s*\\|)+\\s*\\n(?:\\|[^\\n]+\\|\\s*\\n?)+)\",
                text,
            )
            if mt:
                headers, rows = _parse_csv_block(mt.group(1))
        if headers and rows and len(rows) >= 1:
            fm = re.search(r\"交付文件[：:]\\s*([^\\s\\n]+\\.xlsx)\", text, re.I)
            filename = _safe_name(fm.group(1) if fm else \"报表.xlsx\", \"报表.xlsx\", \".xlsx\")
            blob = _build_xlsx(headers, rows)
            prev = (
                \"| \"
                + \" | \".join(headers)
                + \" |\\n| \"
                + \" | \".join([\"---\"] * len(headers))
                + \" |\\n\"
                + \"\\n\".join(
                    \"| \" + \" | \".join(str(c) for c in r) + \" |\" for r in rows[:20]
                )
            )
            xlsx_item = {
                \"filename\": filename,
                \"mime\": \"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\",
                \"blob\": blob,
                \"preview\": f\"```markdown\\n{prev}\\n```\",
            }
"""

# Use actual content from file without double escaping
old = r'''    # ---- XLSX candidate ----
    want_xlsx = bool(
        re.search(r"交付文件[：:]\s*[^\s\n]+\.xlsx", text, re.I)
        or re.search(r"```(?:csv|tsv|table-json|table)", text, re.I)
        or re.search(r"\.xlsx", text, re.I)
    )
    xlsx_item = None
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
            xlsx_item = {
                "filename": filename,
                "mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "blob": blob,
                "preview": f"```markdown\n{prev}\n```",
            }
'''

new = r'''    # ---- XLSX candidate (S4.1: strip delivery chrome; reject nested list tables) ----
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
'''

if old not in src:
    raise SystemExit("xlsx block not found")
src = src.replace(old, new, 1)

end_return = r'''    return {
        "has_file": "no",
        "filename": "",
        "answer": text if text.strip() else "失败：未能生成可下载产物，请补充主题后重试。",
        "download_marker": "NO_FILE",
    }
'''
end_new = r'''    # S4.1: explicit xlsx ask but only nested 交付清单 tables / no business csv
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

    return {
        "has_file": "no",
        "filename": "",
        "answer": text if text.strip() else "失败：未能生成可下载产物，请补充主题后重试。",
        "download_marker": "NO_FILE",
    }
'''
if end_return not in src:
    raise SystemExit("end return not found")
src = src.replace(end_return, end_new, 1)

out1 = ROOT / "ops/evidence/general-wb/s4.1/packdownload_s4.1.py"
out2 = ROOT / "deploy/packdownload/packdownload_s4.1.py"
out1.write_text(src, encoding="utf-8")
out2.write_text(src, encoding="utf-8")
import py_compile

py_compile.compile(str(out1), doraise=True)
print("wrote", out1, out1.stat().st_size)


if __name__ == "__main__":
    pass
