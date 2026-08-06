# 证据 · S1.1-HOTFIX

```
DATE: 2026-08-06
CLAIM-S1.1-HOTFIX: YES
H1–H5: 全绿
```

## 文件

| 路径 | 说明 |
|------|------|
| `gate-H1.md` … `gate-H5.md` | 门禁 |
| `probe-public.txt` | 公网探针 |
| `experts/index.html` · `catalog.yaml` | 部署归档 |
| `ui/ui-*.png` | ≥4 浏览器截图 |
| `s1.1-meta.json` | 元数据 |
| `_capture_ui.py` · `_fix_site_title.py` | 执行脚本（无密钥） |

## 部署

- 源：`deploy/aivia-experts/index.html`
- 现网：`/var/www/aivia-experts/index.html`（ECS + dmit 边缘）
