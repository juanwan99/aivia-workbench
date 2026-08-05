# 阶段 A 执行大包（写实版）

```
STATUS: 功能出口 CLOSED（2026-08-05）· 入口硬化见 PHASE-A-CLOSEOUT.md
DATE: 2026-08-05
对齐: docs/CANON.md · HANDOFF · GOLD-PATHS
出口: G0 + G0b + G1 + G1+ → PIN 已记 PASS
```

> **新执行：** 不要从 A0 重装。先读 [`PHASE-A-CLOSEOUT.md`](./PHASE-A-CLOSEOUT.md) 与 [`upstream/PIN.md`](../upstream/PIN.md)。

## 0. 产品底线

| 用户默认真相 | A 要求 |
|--------------|--------|
| 打开就能进 | G0 |
| 一句话有反应 | G0b DeepSeek |
| 要文件有文件 | G1 可下载 |
| 改一版还有文件 | G1+ |
| 失败不装成功 | G4（建议；A 收口时未测） |

## 1–2. 范围与步骤

历史执行顺序：A0 摸底 → A1 Docker Dify → A2 反代 workbench → A3 G0 → A4 G0b → A5 默认入口「Aivia 课件（阶段A）」→ A6 G1 → A7 G1+ → A9 回写 PIN。  
安装摘要仍见 [`INSTALL.md`](./INSTALL.md)。

## 3. 完成定义（功能）— 已满足

```text
[x] G0 PASS
[x] G0b PASS
[x] G1 PASS
[x] G1+ PASS
[x] 默认入口存在
[x] PIN 已填
[x] Issue #1 已更新（收口）
[ ] 正式 HTTPS 无警告   ← CLOSEOUT R-A1
[ ] 公网稳定可达       ← CLOSEOUT R-A2
[ ] G4 已测             ← CLOSEOUT R-A3
```

## 4. 关联

| 文件 | 用途 |
|------|------|
| `ops/PHASE-A-CLOSEOUT.md` | **收口与残留** |
| `upstream/PIN.md` | 版本与验收 |
| `docs/GOLD-PATHS.md` | 金路径定义 |
| `ops/G-PATH-RUNBOOK.md` | 勾选清单 |
