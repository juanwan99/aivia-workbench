# gate-F3 · C2 同会话 v2 语义真绿

```
DATE: 2026-08-06
RESULT: PASS
```

| 检查 | 结果 |
|------|------|
| 同 conversation_id | **PASS** |
| 新 /dl id | **PASS** |
| 全链接 200 | **PASS** |
| sheet 含市占率 | **PASS** |
| sheet 含产品C + 89/150/20 | **PASS** |
| 营收 11880/15800/13350 | **PASS** |
| 非交付清单套娃 | **PASS** · nested_detect exit 0 |
| 展示名 表格-竞品-v2.xlsx | **PASS**（UTF-8 CD） |
| ≠ 报表.xlsx 默认皮 | **PASS** |

cells：`产品 单价 月销量 估算月营收 市占率 … 产品C 89 150 13350 20%`  
证据：`artifacts/c2-v2.xlsx` · `c2-r2.answer.txt`
