# 标准任务卡 · SCENE-FULL（唯一）

```
════════════════════════════════════════════════════════
标准任务卡 · PHASE-SCENE-FULL（单包单卡）
════════════════════════════════════════════════════════
执行窗：本地浏览器真测 + 云端改 Dify/提示/工作流
上下文：CLEAR
  已收 CLAIM-B · DOC-SOLID · DL-FIX(/dl) · E1 · hybrid
  正式上线=否 · full real=否 · Harness=否
角色：个人全场景打通（对标 WorkBuddy 行为 · clean-room）
口径：内容主靠模型 API；产品保证多场景能下能开能改、失败诚实
RISK: 黄（串台/模型波动/下载回退 data-URL）
FAST: 否 · 按矩阵格子过，禁只跑单条金路径充数
仓：juanwan99/aivia-workbench
BASE：https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl

【真源】
  ops/PHASE-SCENE-FULL-PACK.md
  ops/SCENE-FULL-RUNBOOK.md
  本卡
  docs/CANON.md

【硬门禁·回写】缺一禁止报完毕
  1) SCENE-FULL-RUNBOOK 填满并 push main
  2) ops/evidence/scene-full/（产物+/dl 链样本）
  3) ops/SCENE-FULL-REPORT.md
  4) PIN CLAIM-SCENE-FULL=YES|BLOCKED
  5) CANON/HANDOFF/README 一句
  6) Issue #1 回写无密钥

【做·按序】
  F0 钉 /dl 主路径、禁 data-URL 主路径
  F1 S1–S4 内容场景（课件/教案/表/大纲）· 多说法
  F2 S5 改稿 · S6 拒写库 · S7 连续三任务 · S8 点下无 blocked
  F3 空成功0 · 债表 · P1 可选
  F4 回写 CLAIM-SCENE-FULL

【本地测强制】
  浏览器发送 → 点 https://workbench.../dl/... → 系统应用打开 → 进仓
  出现 [blocked] 或 data: 主路径 = 本包 FAIL

【不做】
  重训/替换模型当主线 · 拆 WorkBuddy 闭源
  假 1:1 功能列表完成 · 全校上线 · 假 full real
  Harness/OpenWork 主线 · 空成功 · 口头完毕 · 密钥进 Git
  仅 API 烟测代替浏览器点下

【出口】
  CLAIM-SCENE-FULL ⇔ S1–S8 全 PASS + /dl 主路径 + 空成功0 + 回写齐
  ≠ 正式上线 · ≠ WorkBuddy 源码级复制 · ≠ 模型重造
════════════════════════════════════════════════════════
```
