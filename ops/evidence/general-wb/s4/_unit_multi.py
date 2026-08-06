#!/usr/bin/env python3
"""Local unit test for S4 multi-pack (no network, mock upload)."""
from __future__ import annotations

import importlib.util
from pathlib import Path

p = Path(__file__).resolve().parent / "packdownload_s4.py"
spec = importlib.util.spec_from_file_location("pack_s4", p)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)

uploads: list[str] = []


def fake_upload(filename: str, mime: str, blob: bytes):
    uploads.append(filename)
    return {
        "ok": True,
        "url": f"https://asyncova.com/dl/id{len(uploads)}/{filename}",
        "filename": filename,
    }


mod._upload = fake_upload  # type: ignore

sample = """
这里是小结

```markdown
# 项目小结
本周完成了 A/B 两项。
## 风险
无重大风险
## 下周
继续推进
```
交付文件：文档-项目小结.docx

```csv
任务,负责人,状态
A,张三,进行中
B,李四,完成
C,王五,待办
```
交付文件：表格-任务进度.xlsx
"""

r = mod.main(sample)
print("marker", r["download_marker"])
print("filename", r["filename"])
print("uploads", uploads)
print("dl_count", r["answer"].count("https://asyncova.com/dl/"))
assert r["download_marker"] == "DOWNLOAD_READY", r
assert len(uploads) == 2, uploads
assert "文档-项目小结" in r["answer"]
assert "表格-任务进度" in r["answer"]
print("UNIT multi PASS")
