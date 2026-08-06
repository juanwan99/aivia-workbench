# 标准任务卡 · WB-FIX-DEPLOY（修复+部署 · 完整）

```
════════════════════════════════════════════════════════
标准任务卡 · PHASE-WB-FIX-DEPLOY（单包单卡 · 无人值守）
════════════════════════════════════════════════════════
执行窗：本机 Grok + SSH 云端 + 本机浏览器/Office
上下文：CLEAR
  CLAIM-WB-ALIGN=YES（有条件）· 深度审查残留待消化
  正式上线=否 · /dl 主路径 · bridge 0.2.2 基线
角色：修复等价偏弱项 + 现网部署加固 + 高标准回归
模式：F0→F4 串行 · 每阶段 gate 自审 → FAIL 修 → PASS 才下阶段
      中途不请示放行；结束或 BLOCKED 回写 Issue
RISK: 黄高（现网 restart；限流；TLS；禁密钥；禁写库）
FAST: 否
仓：juanwan99/aivia-workbench
BASE：https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl
主路径：https://workbench.aivia.asia/dl/...

【真源】
  ops/PHASE-WB-FIX-DEPLOY-PACK.md
  ops/WB-FIX-DEPLOY-RUNBOOK.md
  ops/WB-ALIGN-REPORT.md（残留）
  ops/WB-FEATURE-MATRIX.md
  docs/CANON.md
  本卡

【硬门禁·回写】
  1) gate-F0..F4 全 PASS 于 ops/evidence/wb-fix-deploy/
  2) R1–R8 均有证据或书面缓解
  3) WB-FIX-DEPLOY-NOTES.md（部署/回滚）
  4) WB-FIX-DEPLOY-REPORT.md
  5) PIN CLAIM-WB-FIX-DEPLOY=YES|BLOCKED
  6) CANON/HANDOFF/DEBT/README + Issue + push
  7) 空成功=0 · 无 data-URL 主路径 · 无 [blocked] · 无密钥

【阶段过线·高标准】
  F0 基线：bridge 版本/健康 · /dl 抽测 · 无 secret 进仓
  F1 交付加固：交付清单模板 · DOCX×2 真 OOXML · 弱指令大纲无 DOWNLOAD
  F2 上传再加工：真文件进入任务并出 /dl 产物（可复现步骤）
  F3 部署：现网 ops metrics/policy 烟测 · TLS 实况写入 · 回滚节
  F4 终回归：三格式+大纲+拒写+上传链 · 真源回写 · FINAL

【本地测强制】
  浏览器点 /dl · Office 打开 · 上传路径按 NOTES 复现
  管理接口仅脱敏 json 进仓

【不做】
  重开全量 WB 1:1 · 专家完整壳当本包必做
  full real / 正式上线运营 · 跳阶段假绿 · Agent 写库

【出口】
  CLAIM-WB-FIX-DEPLOY ⇔ F0–F4 PASS + 部署可演示 + 回写齐
  ≠ 自动全校上线 ≠ WorkBuddy 1:1
════════════════════════════════════════════════════════
```
