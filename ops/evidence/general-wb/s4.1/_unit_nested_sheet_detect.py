#!/usr/bin/env python3
"""Detect 'delivery-list nested as sheet' anti-pattern. Exit 0 if nested (bad)."""
import re, sys
from pathlib import Path

def is_nested_delivery_sheet(cells: list[str]) -> bool:
    joined = " ".join(cells)
    has_meta = all(k in joined for k in ("文件名", "类型", "下载")) or (
        "#" in cells and "文件名" in cells and "下载" in cells
    )
    has_biz = any(k in joined for k in ("单价", "月销", "市占率", "营收", "产品A", "产品B"))
    has_dl = "asyncova.com/dl" in joined or "/dl/" in joined
    return bool(has_meta and has_dl and not has_biz)

def cells_from_xlsx(path: Path) -> list[str]:
    import zipfile
    with zipfile.ZipFile(path) as z:
        sheet = next(n for n in z.namelist() if "worksheets/sheet" in n)
        xml = z.read(sheet).decode("utf-8", "ignore")
    return re.findall(r"<t[^>]*>([^<]*)</t>", xml)

if __name__ == "__main__":
    p = Path(sys.argv[1])
    cells = cells_from_xlsx(p)
    nested = is_nested_delivery_sheet(cells)
    print({"path": str(p), "cells": cells[:30], "nested_delivery_sheet": nested})
    # exit 1 if nested (caller expects fail on bad artifact)
    sys.exit(1 if nested else 0)
