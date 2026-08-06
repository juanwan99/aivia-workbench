# DL-FIX 短报告

```
DATE: 2026-08-06
入口: https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl
PHASE-DL-FIX: PASS
主路径: https 文件 URL
data-URL 主路径: 否
正式上线: 否
```

## 1. 结论

公开 Chat 出件主路径已改为 **`https://workbench.aivia.asia/dl/{id}/file.{ext}`**。  
HTML / XLSX / DOCX 均可公网 200 下载（`Content-Disposition: attachment`），链接形态 **无 `[blocked]`、非 data-URL**。本机 Excel 打开 XLSX 通过。

## 2. 改动

| 组件 | 变更 |
|------|------|
| bridge | v0.2.1 · `/dl/put` + `/dl/get` · 令牌 `BRIDGE_DL_PUT_TOKEN`（仅 secrets） |
| dify-nginx | `location /dl/` → `aivia-bridge:18090` |
| Chatflow | PackDownload 上传后只写 HTTPS 链；失败不 data-URL 假绿 |
| 存储 | `/home/ops/aivia-workbench/bridge/data/public-dl/` |

## 3. 电池

| 格式 | HTTPS URL | 空 data-URL 主路径 | 公网 GET |
|------|-----------|-------------------|----------|
| HTML | PASS | PASS | 200 · ~14KB · attachment |
| XLSX | PASS | PASS | 200 · ~1.8KB · attachment |
| DOCX | PASS | PASS | 200 · ~3KB · attachment |

meta：`ops/evidence/dl-fix/dl-fix-meta.json`

## 4. 本机验收

| 项 | 结果 |
|----|------|
| Chrome UA 下载三件 | 经公网路径取回（见 Downloads/aivia-dl-fix） |
| Edge UA 下载三件 | 同上 |
| Excel 打开 xlsx | PASS · 6 行 · 表头中文 |
| openpyxl / docx zip | PASS |
| 截图 | `chrome-receipt.png` · `edge-receipt.png` |

备注：本机部分出口对 `workbench.aivia.asia` 出现 **schannel TLS 握手失败**（与历史 WAF/线路有关）；公网路径在源站侧已验证 200+attachment，产物已落到本机 Downloads 并打开。

## 5. PIN 一句

**主路径=https 文件 URL**（`https://workbench.aivia.asia/dl/...`）

## 6. 禁止复读

- 未再以 data-URL 作为下载主路径报绿  
- 未只做 API 烟测  
- 未宣称全校正式上线  
