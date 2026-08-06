#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CSV 数值列均值 · S2.1：空 stdin / 无参均回落内置示例（修 isatty 脚枪）"""
import sys
import csv
import io

SAMPLE_DATA = """name,age,score,height
Alice,25,88.5,165
Bob,30,92.0,175
Carol,28,79.5,160
"""


def read_csv_from_file(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def compute_column_means(csv_text: str):
    reader = csv.DictReader(io.StringIO(csv_text))
    if not reader.fieldnames:
        print("错误: CSV 没有表头", file=sys.stderr)
        sys.exit(1)
    columns = {name: [] for name in reader.fieldnames}
    for row in reader:
        for name in reader.fieldnames:
            value = (row.get(name) or "").strip()
            if not value:
                continue
            try:
                columns[name].append(float(value))
            except ValueError:
                pass
    means = {}
    for name, values in columns.items():
        means[name] = (sum(values) / len(values)) if values else None
    return reader.fieldnames, means


def main() -> None:
    csv_text = None
    if len(sys.argv) > 1:
        try:
            csv_text = read_csv_from_file(sys.argv[1])
        except FileNotFoundError:
            print(f"错误: 文件 '{sys.argv[1]}' 不存在", file=sys.stderr)
            sys.exit(1)
    elif not sys.stdin.isatty():
        data = sys.stdin.read()
        # S2.1 fix: empty redirect/pipe → sample, not "无表头"
        csv_text = data if data.strip() else SAMPLE_DATA
        if not data.strip():
            print("标准输入为空，使用内置示例数据:", file=sys.stderr)
    else:
        print("未提供输入，使用内置示例数据:", file=sys.stderr)
        csv_text = SAMPLE_DATA

    fieldnames, means = compute_column_means(csv_text)
    print("\n=== 数值列均值统计 ===")
    print(f"{'列名':<15} {'均值':>10}")
    print("-" * 28)
    for name in fieldnames:
        mean = means[name]
        if mean is not None:
            print(f"{name:<15} {mean:>10.4f}")
        else:
            print(f"{name:<15} {'(非数值)':>10}")
    numeric_cols = sum(1 for v in means.values() if v is not None)
    print("-" * 28)
    print(f"共 {len(fieldnames)} 列，其中 {numeric_cols} 列为数值列")


if __name__ == "__main__":
    main()
