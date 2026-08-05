# Skills（本仓）

此处放置 **Aivia 自研** 技能。格式遵循 OpenCode / OpenWork Skill 规范：

```text
skills/<skill-id>/SKILL.md
```

- `name` 与目录名一致，小写+连字符
- `description` 写清触发场景（供模型选择）
- 需要文件时：**必须**要求使用写盘工具，并在成功时给出路径

## 当前技能

| ID | 目录 | 阶段 | 说明 |
|----|------|------|------|
| courseware-html | `skills/courseware-html/` | B | 课件 HTML，强制落盘 |
| lesson-plan-docx | `skills/lesson-plan-docx/` | B | 教案 DOCX 骨架，强制落盘 |

## 导入

1. OpenWork → Skills 管理器 → 导入本目录下文件夹  
2. 或复制到工作区：`.opencode/skills/<id>/SKILL.md`  
3. 或用户级：`~/.config/opencode/skills/<id>/SKILL.md`

**阶段 A：** 可只用上游默认写文件工具跑 G1。  
**阶段 B：** G1 绿后启用上述 Skills，配合 `docs/DELIVERY-RULES.md` 清零空成功。
