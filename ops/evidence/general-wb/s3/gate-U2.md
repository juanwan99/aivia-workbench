# gate-U2 · 要文件：下载可见可下 · 展示名贴题

```
DATE: 2026-08-06
RESULT: PASS
```

| 检查 | 结果 |
|------|------|
| 浏览器可见「交付清单」完成投影 | **PASS** |
| HTTPS `/dl` 链接可点 | **PASS** · `https://asyncova.com/dl/fa4eaa08bf4d4942afeb4502f4c75e80/file.docx` |
| 公网 GET 200 · OOXML | **PASS** · size=2438 · PK zip |
| 展示名贴题 ≠ 教案.docx | **PASS** · **文档-S3体感验收周报.docx** |
| Content-Disposition UTF-8 文件名 | **PASS** · `filename*=UTF-8''…S3体感验收周报.docx` |
| DOWNLOAD_READY | **PASS** |

证据：`ui/u2-file-dl.png` · `u2-week-report.docx` · `probe-u2-retry.json`
