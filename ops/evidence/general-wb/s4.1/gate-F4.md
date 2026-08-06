# gate-F4 · 电池语义 + 套娃样本 FAIL

```
DATE: 2026-08-06
RESULT: PASS
```

| 检查 | 结果 |
|------|------|
| C2 断言：市占/产品C/营收/非套娃/全 200 | **PASS** |
| 旧坏表 `s4/artifacts/c2-v2.xlsx` nested detect exit 1 | **PASS**（识别为坏） |
| pack unit 套娃输入 → NO_FILE | **PASS** |

脚本：`_battery_f3456.py` · `_unit_pack_s41.py` · `_unit_nested_sheet_detect.py`
