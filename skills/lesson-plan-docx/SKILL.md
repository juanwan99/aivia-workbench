---
name: lesson-plan-docx
description: 生成教案。现行默认可下载真 DOCX；亦支持 Markdown（.md）。
license: MIT
compatibility: dify
metadata:
  audience: teachers
  workflow: lesson-plan
  aivia: "true"
  format_scope: "docx-primary-md-fallback"
---

# 教案（Dify Web）

## 现行 scope（2026-08-06 DOC-SOLID）

- **优先产物：DOCX**（`交付文件：教案-<主题>.docx` + 完整 ```markdown 正文；Code 节点打成 OOXML）
- **Markdown 仍可用**：用户明确只要 MD 时 `交付文件：…md`
- 本机 Word/WPS 可打开；非 OnlyOffice 精修模板

## 强制纪律

1. 用户要教案/Word/可下载文件 → 必须给完整可保存产物。
2. 无产物不得说完成。
3. 结构：课题、目标、重难点、过程、作业。
4. 同会话改稿：输出完整新文件。
