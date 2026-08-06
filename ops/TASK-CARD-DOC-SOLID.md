# 标准任务卡 · DOC-SOLID（唯一）

```
════════════════════════════════════════════════════════
标准任务卡 · PHASE-DOC-SOLID（单包单卡）
════════════════════════════════════════════════════════
执行窗：同时具备「本地浏览器真测」+「云端改 Dify/仓」
上下文：CLEAR
  已收 P0-GATE · CLAIM-B=YES · E1 · hybrid
  正式上线=否 · full real=否 · Harness=否
角色：文档/报表交付做扎实（对标 WorkBuddy 行为 · clean-room）
RISK: 黄（工作流/文件节点；体积；禁密钥进仓；禁 Agent 写库）
FAST: 否 · 边测边改 · 按 S0→S5
仓：juanwan99/aivia-workbench
BASE：https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl
      （若改入口必须写 PIN）

【真源】
  ops/PHASE-DOC-SOLID-PACK.md
  ops/DOC-SOLID-RUNBOOK.md
  本卡
  docs/CANON.md

【硬门禁·回写】缺一禁止报完毕
  1) 填满 DOC-SOLID-RUNBOOK 并 push main
  2) ops/evidence/doc-solid/ 含本地可开的 xlsx（+docx 或 md+债）
  3) ops/DOC-SOLID-REPORT.md
  4) PIN/CANON/HANDOFF 一句 CLAIM-DOC-SOLID
  5) Issue #1「DOC-SOLID PASS|BLOCKED」无密钥

【做·按序】
  S0 钉本地测+云端改 · 冷启动
  S1 真 XLSX 报表可下 · 本地 Excel/WPS 打开 · 同会话改稿
  S2 DOCX 优先；不能则 MD+docx-debt 诚实
  S3 R-G1/G3/G4/X · 空成功=0
  S4 推荐问题加表/文档 · 禁装饰假按钮
  S5 回写收口

【本地测强制】
  每条主路径：浏览器发送 → 下载 → 系统应用打开 → 文件进仓
  API 烟测不能替代本地打开

【不做】
  一次上齐 PPT/PDF/全格式 · 假 WorkBuddy 全量
  Harness/OpenWork 主线 · 全校上线 · 假 full real
  空成功 · 口头完毕 · 密钥进 Git · Agent 写成绩库

【出口】
  CLAIM-DOC-SOLID PASS ⇔ S1 硬绿 + S2 诚实满绿或债 + S3 空成功0 + 回写齐
  ≠ 正式上线 · ≠ WorkBuddy 功能 1:1
════════════════════════════════════════════════════════
```
