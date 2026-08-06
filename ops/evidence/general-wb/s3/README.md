# 证据 · S3-UX + S3-DELIVER

```
DATE: 2026-08-06
CLAIM-S3-UX: YES（须 main 可见）
U1–U7: 全绿
D1–D6: 全绿
```

## 文件

| 路径 | 说明 |
|------|------|
| `gate-U1.md` … `gate-U7.md` | 体感门禁 |
| `gate-D1.md` … `gate-D6.md` | 交付门禁 |
| `ui/u*.png` | 浏览器截图（8 ≥ 5） |
| `u2-week-report.docx` | U2 真下载产物 |
| `probe-*.json` | 探针 |
| `experts-live.html` · `experts-deploy.html` | /experts 归档 |
| `results.json` · `s3-meta.json` | 汇总 |
| `_capture_ui_s3.py` · `_retry_u2.py` | 脚本（无密钥） |

## 变更

- `/experts` 页脚：行为对标 · ≠像素 · ≠备案完成
- **未改** PackDownload s2.1
- **S3-DELIVER**：git push main，关闭「口头无图 CLAIM」审查债

报告：`ops/S3-UX-REPORT.md` · 详卡：`ops/TASK-CARD-S3-DELIVER.md`
