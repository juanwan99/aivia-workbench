# 标准任务卡 · QUAD-FIX-DEPLOY（修复+部署）

```
════════════════════════════════════════════════════════
标准任务卡 · PHASE-QUAD-FIX-DEPLOY（单包单卡 · 无人值守）
════════════════════════════════════════════════════════
执行窗：本机 Grok + SSH（ECS + 边缘）+ 浏览器
上下文：CLEAR
  CLAIM-QUAD-LAUNCH=YES · 正式上线=是（受限）· FULL-REAL=NO
  深度审查残留：/experts→:8443 · 隧道 nohup · catalog/NOTES 缺
角色：修复阻断体验 + 部署加固 + 文档齐
模式：X0→X4 自审→修→过门 · 中途不请示
RISK: 黄（nginx/隧道；禁密钥；禁扩大上线范围）
FAST: 否 · P0 先修入口
仓：juanwan99/aivia-workbench
公网：https://asyncova.com
Chat：https://asyncova.com/chat/lOMVPbz7rZmbJSJl
专家：https://asyncova.com/experts  （修后无斜杠也必须可用）

【真源】
  ops/QUAD-FIX-SURVEY.md
  ops/PHASE-QUAD-FIX-DEPLOY-PACK.md
  ops/QUAD-FIX-DEPLOY-RUNBOOK.md
  ops/QUAD-LAUNCH-REPORT.md
  docs/CANON.md
  本卡

【硬门禁·回写】
  1) gate-X0..X4 → ops/evidence/quad-fix-deploy/
  2) F1 验收：curl -sI https://asyncova.com/experts | 不得出现 8443
     且最终拿到专家 HTML（200）
  3) F2：ops/edge 下 unit + probe；restart 后 Chat+/experts 200
  4) ops/experts/catalog.yaml + QUAD-FIX-DEPLOY-NOTES.md
  5) QUAD-FIX-DEPLOY-REPORT.md
  6) PIN CLAIM-QUAD-FIX-DEPLOY=YES|BLOCKED
  7) CANON/HANDOFF/DEBT/README + Issue + push
  8) 正式上线仍「是（受限）」· FULL-REAL=NO · 空成功0 · 无密钥

【阶段过线】
  X0 复现坏 302 与基线
  X1 修 nginx 专家入口（P0）· 浏览器无斜杠打开
  X2 隧道 systemd 保活 + 探活（P0）· 重启回归
  X3 catalog.yaml + 部署回滚 NOTES + 链接纠正
  X4 金路径 /dl + 专家 1 卡 + 真源回写

【本地测强制】
  浏览器打开「无尾斜杠」专家链接
  浏览器打开 Chat 要 1 个可下载文件

【不做】
  full real · 全校推广 · 假 1:1 · 只写文档不修 8443
  密钥进仓 · Agent 写库

【出口】
  CLAIM-QUAD-FIX-DEPLOY ⇔ F1+F2 硬绿 + 文档齐 + 回归 + 回写
  ≠ 备案完成 ≠ FULL-REAL ≠ 全校上线
════════════════════════════════════════════════════════
```
