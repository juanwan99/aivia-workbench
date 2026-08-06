# 标准任务卡 · P0-GATE（唯一）

```
════════════════════════════════════════════════════════
标准任务卡 · PHASE-P0-GATE（单包单卡 · 重新派发）
════════════════════════════════════════════════════════
执行窗：现网运维 + 产品验收（可同一人串行）
上下文：CLEAR
  已收 A/B/C-hybrid/D-LITE/E1
  未收 CLAIM-B · full real（可选）· 正式上线
角色：稳定 + 金路径体感 + CLAIM-B 一次收口
RISK: 黄（TLS/WAF/nginx；模型波动；禁密钥进仓；禁公网裸 bridge）
FAST: 否 · 按段 A→B→C 顺序做完
仓：juanwan99/aivia-workbench
BASE：https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl

【真源】
  ops/PHASE-P0-GATE-PACK.md
  ops/P0-GATE-RUNBOOK.md
  本卡

【硬门禁·回写】缺一禁止报完毕、禁止勾 CLAIM-B
  1) 填满 ops/P0-GATE-RUNBOOK.md 并 push main
  2) ops/evidence/p0-gate/ 真产物
  3) ops/P0-GATE-REPORT.md + ops/CLAIM-B-SCRIPT.md
  4) PIN：CLAIM-B=YES（若 C 过）· 正式上线=否
  5) CANON/HANDOFF/README/DEBT 一句
  6) Issue #1「P0-GATE PASS|BLOCKED」无密钥

【做 · 按序】
  段A 公网TLS连测≥3 · 桌面+4G有壳 · 续期策略 · 真源去旧句 · bridge health
  段B G1 / G1+ / G2 / G3 / G4 · 空成功=0 · 证据进仓
  段C CLAIM-B：桌面+4G · 可下可改 · 五句话术 · PIN CLAIM-B=YES
  段D edu API 有则 full real；无则书面跳过 hybrid

【不做】
  拆多卡分别假绿 · 跳过 A/B 勾 CLAIM-B
  假 full real · 全校推广 · Harness/OpenWork 主线
  Agent 写库 · 关限流刷数 · 密钥/AK 进 Git

【出口】
  P0-GATE PASS ⇔ A+B+C 全过 + 回写齐
  CLAIM-B 随 C；正式上线默认否
  D 跳过不扣整包（须声明）
════════════════════════════════════════════════════════
```
