# 任务包 · PHASE-DL-FIX（下载解 blocked）

```
STATUS: PASS · 2026-08-06
CODE: PHASE-DL-FIX
前提: CLAIM-DOC-SOLID=YES · CLAIM-B=YES · 正式上线=否
唯一目标: 公开 Chat 点「下载」→ 浏览器真开始下文件（HTML/XLSX/DOCX）
主路径: https 文件 URL（https://workbench.aivia.asia/dl/...）
禁止: 只修 API 烟测 · 继续只靠 data-URL 报绿
```

## 根因

旧 PackDownload 用 **data-URL** 作「点击下载」链接。Chrome/Edge 对大体积 / 部分 MIME 的 `data:` 链接会标 **[blocked]**，用户点了不会真下载。

## 解法

1. **aivia-bridge v0.2.1** 增加公开落盘：`POST /dl/put`（令牌）+ `GET /dl/{id}/file.ext`（公开）  
2. **dify-nginx** `location /dl/` 反代到 bridge  
3. **Chatflow Code** 上传后只输出 `https://workbench.aivia.asia/dl/...`（失败诚实，不回退 data-URL 报绿）  
4. URL 路径仅 ASCII `file.{ext}`；真实中文名在 `Content-Disposition: filename*`

## 验收

| 项 | 结果 |
|----|------|
| Chat 回答含 DOWNLOAD_READY + https 链 | PASS · 无 data-URL 主路径 |
| HTML/XLSX/DOCX 公网 GET 200 + attachment | PASS |
| 本机打开 xlsx/docx/html | PASS |
| Chrome/Edge 证据截图 | `ops/evidence/dl-fix/*-receipt.png` |
| PIN 一句主路径 | 见 `upstream/PIN.md` |

## 证据

`ops/evidence/dl-fix/` · `ops/DL-FIX-REPORT.md`
