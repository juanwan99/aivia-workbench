#!/usr/bin/env python3
"""Build packdownload_fixed.py from dumped wf code with R2-R4 fixes; scrub secrets."""
from __future__ import annotations

import re
from pathlib import Path

src = Path(__file__).with_name("wf-packdownload.py")
code = src.read_text(encoding="utf-8")
code = re.sub(r'DL_PUT_URL\s*=\s*"[^"]*"', 'DL_PUT_URL = "__DL_PUT_URL__"', code)
code = re.sub(r'DL_PUT_TOKEN\s*=\s*"[^"]*"', 'DL_PUT_TOKEN = "__DL_PUT_TOKEN__"', code)

old_pack_answer = """    url = up[\"url\"]
    answer = (
        f\"交付文件：{filename}\\n\\n\"
        f\"DOWNLOAD_READY\\n\\n\"
        f\"[点击下载 {filename}]({url})\\n\\n\"
        f\"下载链接（HTTPS）：{url}\\n\\n\"
        f\"（浏览器将直接下载文件；主路径为 https 文件 URL，非 data-URL）\\n\\n\"
        f\"<details><summary>内容预览（备用）</summary>\\n\\n{preview}\\n\\n</details>\"
    )"""
new_pack_answer = """    url = up[\"url\"]
    answer = (
        f\"## 交付清单\\n\"
        f\"| # | 文件名 | 类型 | 下载 |\\n\"
        f\"|---|--------|------|------|\\n\"
        f\"| 1 | {filename} | {mime.split(';')[0]} | [点击下载]({url}) |\\n\\n\"
        f\"DOWNLOAD_READY\\n\\n\"
        f\"- **文件名**：{filename}\\n\"
        f\"- **HTTPS**：{url}\\n\"
        f\"- **主路径**：https 文件 URL（非 data-URL）\\n\\n\"
        f\"[点击下载 {filename}]({url})\\n\\n\"
        f\"<details><summary>内容预览（备用）</summary>\\n\\n{preview}\\n\\n</details>\"
    )"""
if old_pack_answer not in code:
    raise SystemExit("pack answer block not found")
code = code.replace(old_pack_answer, new_pack_answer)

helper = '''

def _is_outline_only(text: str) -> bool:
    t = text or ""
    if re.search(r"交付文件[：:]\\s*\\S+\\.(html|docx|xlsx|md)\\b", t, re.I):
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
    m = re.search(r"```(?:markdown|md)\\s*(.*?)```", text, re.S | re.I)
    if m:
        return m.group(1).strip()
    if re.search(r"(课题|教学目标|教学过程|作业)", text) and len(text) > 80:
        body = re.sub(r"交付文件[：:].*", "", text)
        body = re.sub(r"```.*?```", "", body, flags=re.S)
        return body.strip() or None
    return None

'''
if "_is_outline_only" not in code:
    code = code.replace("def main(llm_text: str) -> dict:", helper + "\ndef main(llm_text: str) -> dict:")

old_main = '''def main(llm_text: str) -> dict:
    text = llm_text or ""

    # ---- XLSX ----'''
new_main = '''def main(llm_text: str) -> dict:
    text = llm_text or ""
    want_docx = False

    # R4: outline-only hard skip packing
    if _is_outline_only(text):
        clean = re.sub(r"DOWNLOAD_READY\\s*", "", text)
        clean = re.sub(r"https://workbench\\.aivia\\.asia/dl/\\S+", "", clean)
        return {
            "has_file": "no",
            "filename": "",
            "answer": clean.strip() or text,
            "download_marker": "NO_FILE",
        }

    # ---- XLSX ----'''
if old_main not in code:
    raise SystemExit("main start not found")
code = code.replace(old_main, new_main)

old_docx = '''    # ---- DOCX ----
    fm_docx = re.search(r"交付文件[：:]\\s*([^\\s\\n]+\\.docx)", text, re.I)
    md_block = re.search(r"```(?:markdown|md)\\s*(.*?)```", text, re.S | re.I)
    if fm_docx and md_block:
        md = md_block.group(1).strip()
        filename = _safe_name(fm_docx.group(1), "教案.docx", ".docx")
        blob = _build_docx_from_md(md)
        return _pack(
            filename,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            blob,
            f"```markdown\\n{md[:4000]}\\n```",
        )'''
new_docx = '''    # ---- DOCX (R3 harden) ----
    fm_docx = re.search(r"交付文件[：:]\\s*([^\\s\\n]+\\.docx)", text, re.I)
    want_docx = bool(fm_docx) or (
        bool(re.search(r"(教案|Word|DOCX|\\.docx)", text, re.I)) and not want_xlsx
    )
    md = _extract_md(text)
    if want_docx and md and not re.search(r"```html", text, re.I):
        filename = _safe_name(fm_docx.group(1) if fm_docx else "教案.docx", "教案.docx", ".docx")
        blob = _build_docx_from_md(md)
        return _pack(
            filename,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            blob,
            f"```markdown\\n{md[:4000]}\\n```",
        )'''
if old_docx not in code:
    raise SystemExit("docx block not found")
code = code.replace(old_docx, new_docx)

code = code.replace(
    """    # ---- Markdown fallback ----
    if md_block:
        md = md_block.group(1).strip()""",
    """    # ---- Markdown fallback (skip if docx intent) ----
    md_block = re.search(r"```(?:markdown|md)\\s*(.*?)```", text, re.S | re.I)
    if md_block and not want_docx:
        md = md_block.group(1).strip()""",
)

out = Path(__file__).with_name("packdownload_fixed.py")
out.write_text(code, encoding="utf-8")
print("wrote", out, "len", len(code))
for line in code.splitlines():
    if "DL_PUT_TOKEN" in line or "DL_PUT_URL" in line:
        print(line)
