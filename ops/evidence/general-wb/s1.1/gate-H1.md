# gate-H1 · /experts 通用化部署

```
DATE: 2026-08-06
RESULT: PASS
```

| 检查 | 结果 |
|------|------|
| 无「面向教师备课出件」 | **PASS**（公网 HTML 无此句） |
| 有「通用」 | **PASS** |
| 办公 Word / Excel / 公号 / 代码 / 短答 / 改稿 | **PASS**（页面 6 张通用卡） |
| 教育最多 1 张且标「可选领域」 | **PASS**（1 张 · badge/标题含可选领域） |
| 源站 `/var/www/aivia-experts/index.html` | **已部署**（ECS） |
| 边缘 `/var/www/aivia-experts/index.html` | **已同步**（dmit） |

证据：`experts/index.html` · `ui/ui-experts.png` · `probe-public.txt`
