#!/usr/bin/env python3
"""Unit: nested delivery must NO_FILE; good csv packs; multi still works."""
from __future__ import annotations

import importlib.util
from pathlib import Path

p = Path(__file__).resolve().parent / "packdownload_s4.1.py"
spec = importlib.util.spec_from_file_location("pd41", p)
m = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(m)

uploads: list[str] = []


def fake_upload(filename: str, mime: str, blob: bytes):
    uploads.append(filename)
    return {
        "ok": True,
        "url": f"https://asyncova.com/dl/id{len(uploads)}/{filename}",
        "filename": filename,
    }


m._upload = fake_upload  # type: ignore

nested = """## 交付清单
| # | 文件名 | 类型 | 下载 |
|---|--------|------|------|
| 1 | 表格-竞品-v2.xlsx | application/xlsx | [点击下载](https://asyncova.com/dl/2f9d3c8e7b1a4f5d9c6e8a2b7d1f3e5c/file.xlsx) |
DOWNLOAD_READY
交付文件：表格-竞品-v2.xlsx
"""
uploads.clear()
r = m.main(nested)
print("NEST", r["download_marker"], uploads)
assert r["download_marker"] == "NO_FILE" and not uploads

good = """```csv
产品,单价,月销量,市占率,估算月营收
A,99,120,40,11880
B,79,200,60,15800
C,89,150,20,13350
```
交付文件：表格-竞品-v2.xlsx
"""
uploads.clear()
r2 = m.main(good)
print("GOOD", r2["download_marker"], uploads, r2.get("filename"))
assert r2["download_marker"] == "DOWNLOAD_READY", r2
assert uploads and "竞品-v2" in uploads[0], uploads

multi = """```markdown
# 小结
进展 ok
```
交付文件：文档-小结.docx

```csv
任务,负责人,状态
A,张三,进行中
B,李四,完成
C,王五,待办
```
交付文件：表格-进度.xlsx
"""
uploads.clear()
r3 = m.main(multi)
print("MULTI", r3["download_marker"], uploads)
assert r3["download_marker"] == "DOWNLOAD_READY" and len(uploads) == 2

# old s4 nested style: prior list + only meta md table as "data"
nested2 = """
先改一版。
## 交付清单
| # | 文件名 | 类型 | 下载 |
|---|--------|------|------|
| 1 | 表格.xlsx | x | [点击下载](https://asyncova.com/dl/abc/file.xlsx) |

```markdown
| # | 文件名 | 类型 | 下载 |
| --- | --- | --- | --- |
| 1 | 表格-竞品-v2.xlsx | application/vnd... | [点击下载](https://asyncova.com/dl/2f9d3c8e/file.xlsx) |
```
交付文件：表格-竞品-v2.xlsx
"""
uploads.clear()
r4 = m.main(nested2)
print("NEST2", r4["download_marker"], uploads)
assert r4["download_marker"] == "NO_FILE" and not uploads

print("ALL UNIT PASS")
