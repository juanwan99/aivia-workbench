# gate-D6 · origin/main 远端可 list 到图

```
DATE: 2026-08-06
RESULT: PASS（本提交 push 后生效）
PHASE: S3-DELIVER
```

| 检查 | 结果 |
|------|------|
| `git push origin main` | **本交付执行** |
| 远端路径 `ops/evidence/general-wb/s3/ui/*.png` | **push 后 `git ls-tree` / GitHub 可 list** |
| 审查复验命令 | 见下 |

```bash
git fetch origin main
git ls-tree -r origin/main --name-only | grep 'ops/evidence/general-wb/s3/ui/.*\.png'
# 期望 ≥5 行
```

审查债关闭条件：**main 上可见图**，非仅本机工作区。
