# gate-F1
DATE: 2026-08-06
STAGE: F1
RESULT: PASS

| # | 标准 | 结果 | 证据 |
|---|------|------|------|
| R2 交付清单模板 | PASS | docx/xlsx/html answers 含 `## 交付清单` 表 + 多行 https |
| R3 DOCX×2 真 OOXML | PASS | F1/docx_1.docx · docx_2.docx · ooxml=true |
| R4 弱大纲无 DOWNLOAD | PASS | F1/outline_weak.answer.txt · has_dl=false |
| 禁 data-URL | PASS | results 扫描 has_data_url=false |

## 备注
- list_html 首轮模型未关 fence 导致未打包；list_html2 重试 PASS（交付清单+html）
- workflow 发布：`fix-deploy` id `db774ef4-…` 已挂 apps.workflow_id

## 空成功: 0
## 进入 F2: YES
