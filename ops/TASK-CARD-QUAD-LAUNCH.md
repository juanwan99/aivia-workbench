# 标准任务卡 · QUAD-LAUNCH（四线大包 · 完整）

```
════════════════════════════════════════════════════════
标准任务卡 · PHASE-QUAD-LAUNCH（单包单卡 · 无人值守）
════════════════════════════════════════════════════════
执行窗：本机 Grok + SSH 云端 + Win/手机浏览器
上下文：CLEAR
  已收 FIX-DEPLOY/ALIGN/SCENE-FULL；正式上线=否；hybrid；E-01 未建
  业主：上线授权 + 专家壳 + full real + 客户端 TLS 全部做
角色：四线合一落地 · 高标准验收 · 分阶段自审
模式：Q0→Q5 串行 · gate 自审 → FAIL 修 → PASS 下阶段
      中途不请示；结束或 BLOCKED 回写 Issue
RISK: 高（证书/nginx/上线话术/edu 依赖；禁密钥；禁假 full real；禁写库）
FAST: 否
仓：juanwan99/aivia-workbench
BASE Chat：https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl
专家台目标：https://workbench.aivia.asia/experts （可 NOTES 改钉）

【真源】
  ops/QUAD-LAUNCH-SURVEY.md          ← 先读调查
  ops/PHASE-QUAD-LAUNCH-PACK.md
  ops/QUAD-LAUNCH-RUNBOOK.md
  ops/WB-FEATURE-MATRIX.md（E-01/I-06）
  docs/EDU-BRIDGE.md · ops/INFRA.md · docs/CANON.md
  本卡

【硬门禁·回写】
  1) gate-Q0..Q5 + FINAL 于 ops/evidence/quad-launch/
  2) T/E/R/L 证据子目录
  3) LAUNCH-CHECKLIST + LAUNCH-RUNBOOK + LAUNCH-AUTH
  4) experts/catalog.yaml + 专家台部署 NOTES
  5) QUAD-LAUNCH-REPORT + DEPLOY-NOTES
  6) PIN/CANON/README/HANDOFF/DEBT + Issue + push
  7) 空成功=0 · /dl 主路径 · 无密钥 · 无假 full real

【阶段过线·高标准】
  Q0 基线：三格式/dl · 大纲 · 拒写 · bridge 健康
  Q1 TLS：链完整 · Win Chrome+Edge · 手机4G 无证书警告 · 续期策略
         · 至少一端完成下载 · 残余写 T-residual
  Q2 专家壳：公网 /experts · ≥4 卡配置 · ≥2 卡真出件本机打开
  Q3 full real：发现文档必有
         · API 就绪→MODE=real+live 脱敏证据+403+拒写
         · 未就绪→DEGRADED 齐套且 PIN FULL-REAL=NO（不阻塞 L）
  Q4 上线：CHECKLIST 全勾 · 话术含限制 · AUTH 按卡内授权条款落盘
         · CANON 正式上线=是（技术门过后方可）
  Q5 终回归：专家1卡+默认链 · 报告 · 回写

【授权条款·Q4 可用】
  业主已指令四线全做含上线；Q0–Q3 技术门通过（R 允许 DEGRADED）后，
  执行窗可写 LAUNCH-AUTH 并将正式上线置是，必须写明范围与限制。

【不做】
  WorkBuddy 像素抄 · 桌面/IM 全量 · Agent 写库
  edu API 没有却标 full real
  跳过 TLS 直接上线 · 专家花架无出件

【出口】
  CLAIM-QUAD-LAUNCH=YES ⇔ 四线处置齐 + 回写齐
  正式上线=是（Q4）时仍 ≠ 1:1 WorkBuddy
  FULL-REAL 独立字段 YES/NO
════════════════════════════════════════════════════════
```
