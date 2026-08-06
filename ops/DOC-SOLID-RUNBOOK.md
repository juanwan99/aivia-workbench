# DOC-SOLID 勾选（单包单卡）

日期：2026-08-06    执行人：Grok Build（本地+ECS）  
BASE：https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl  
正文：`ops/PHASE-DOC-SOLID-PACK.md`  
证据：`ops/evidence/doc-solid/`

## 硬门禁

- [x] 本文件填满  
- [x] 本地打开过的产物已进仓  
- [x] `ops/DOC-SOLID-REPORT.md`  
- [x] PIN + CANON/HANDOFF 一句  
- [x] Issue #1 + push main  
→ 缺一不得报 CLAIM-DOC-SOLID

## S0

- [x] 本地浏览器 + 云端改码能力确认  
- [x] 冷启动有壳  
- [x] 数据 MODE=fixture  

## S1 XLSX

- [x] S1.1 真 xlsx  
- [x] S1.2 可下载  
- [x] S1.3 本地 Excel/WPS 打开（表头+≥3 行）  
- [x] S1.4 同会话改稿再下  
- [x] 产物路径：`ops/evidence/doc-solid/s1-artifact.xlsx` · `s1-rev-artifact.xlsx`  

## S2 文档

- [x] DOCX 满绿 / MD+docx-debt（圈一）**DOCX 满绿**  
- [x] 改稿  
- [x] 产物路径：`ops/evidence/doc-solid/s2-artifact.docx` · `s2-rev-artifact.docx`  

## S3 回归（空成功须 0）

| ID | 结果 |
|----|------|
| R-G1 HTML | PASS · `r-g1-artifact.html` |
| R-G3 大纲 | PASS · 无假 DOWNLOAD_READY |
| R-G4 拒写库 | PASS · 人话拒绝 |
| R-X XLSX 再跑 | PASS · `r-x-artifact.xlsx` |

空成功次数：**0**

## S4 体感

- [x] 推荐问题含表/文档  

## CLAIM

```text
CLAIM-DOC-SOLID: YES
正式上线: 否
full real: 否（默认 fixture）
DOCX: 满绿
```
