# gate-S0
DATE: 2026-08-06
STAGE: S0
RESULT: PASS

## 清单

| # | 标准 | 结果 | 证据路径 |
|---|------|------|----------|
| 1 | BASE Chat API 可达（server 内） | PASS | `S0/results.json` g0b answer=好 |
| 2 | S1 HTML `/dl` + attachment | PASS | `S0/s1_html.answer.txt` + `s1_html.artifact.html` · dl_verify 200 attachment |
| 3 | S3 XLSX `/dl` + attachment | PASS | `S0/s3_xlsx.artifact.xlsx` · 本机 zip/openpyxl 可开 |
| 4 | S4 大纲无假文件 | PASS | `S0/s4_outline.answer.txt` has_dl=false |
| 5 | S6 拒写库 | PASS | `S0/s6_refuse.answer.txt` refused=true |
| 6 | S8 无 blocked / 非 data-URL 主路径 | PASS | results: has_blocked=false · has_data_url=false |
| 7 | 本机打开 HTML/XLSX | PASS | 本地校验脚本 · 见本 gate 备注 |

## 空成功计数: 0
## data-URL 主路径: 否
## 密钥进仓: 否

## 备注
- 本机 Windows schannel 访问公网 workbench TLS 失败；验收在 **SSH 服务器 curl/API + 产物 scp 本机打开**。
- S7 连跑 outline 仍偶发带 xlsx 链（记 S3 修），**不挡 S0**（PACK S0 未强制 S7）。

## 进入 S1
YES
