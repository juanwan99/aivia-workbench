# gate-F5 · G6 空 stdin 可跑

```
DATE: 2026-08-06
RESULT: PASS
```

| 检查 | 结果 |
|------|------|
| 命令 | `python3 g6-script-fixed.py </dev/null` |
| 退出码 | **0** |
| 行为 | 空 stdin → 内置示例 · 打印 age/score/height 均值 |

证据：`g6-script-fixed.py` · `g6-fixed.run.txt`
