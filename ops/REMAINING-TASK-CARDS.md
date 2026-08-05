# 剩余任务卡（现行）

```
DATE: 2026-08-06
已收: A/B · C-mock · C-FIX · D-LITE
未收: E1 · C-REAL
```

> 两卡可串行：建议 **先 E1（对外信任）** 或 **先 C-REAL（校内身份）**，由业主选。  
> **硬门禁：** 无 RUNBOOK+PIN+Issue 回写 + push main = 不得报完毕。

---

## 卡 A · PHASE-E1（正式 HTTPS）

**包：** `ops/PHASE-E1-PACK.md` · **勾选：** `ops/E1-RUNBOOK.md`

```
════════════════════════════════════
标准任务卡 · PHASE-E1
════════════════════════════════════
执行窗：业主（阿里云 DNS）+ 现网运维（证书/nginx）
上下文：CLEAR · D-LITE 已绿 · CLAIM-B 仍否 · 自签已知
角色：正式 HTTPS + 公网复验
RISK: 黄（证书/nginx；勿裸 stop；AK 勿进 Git）
FAST: 相对独立
仓：juanwan99/aivia-workbench
【硬门禁·回写】
  1) 填满 ops/E1-RUNBOOK.md 并 push main
  2) 更新 PIN + DEBT-LEDGER + INFRA（证书状态）
  3) Issue #1 留「E1 PASS」或「E1 BLOCKED+原因」（无密钥/无 IP）
  4) 缺一 → 禁止报完毕 · 禁止 CLAIM-B
【真源】CANON → PHASE-E1-PACK → E1-RUNBOOK
【做】DNS-01 或云证书 → nginx fullchain → systemctl reload nginx
      → 浏览器无警告 → 默认 Chat 可聊可下载 → 外网/4G 复验
【不做】HTTP-01 死磕、假 CLAIM-B、重刷 B、公网裸 bridge
【CLAIM】E1 PASS 后可谈 CLAIM-B（仍须可聊可下载）
BASE：https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl
════════════════════════════════════
```

---

## 卡 B · PHASE-C-REAL（真身份 + 只读 + Dify 网）

**包：** `ops/PHASE-C-REAL-PACK.md` · **勾选：** `ops/C-REAL-RUNBOOK.md`

```
════════════════════════════════════
标准任务卡 · PHASE-C-REAL
════════════════════════════════════
执行窗：bridge 研发 + edu 对接 + Dify 管理
上下文：CLEAR · C-mock/C-FIX 绿 · C-REAL 未开工 · E1 可并行
角色：真/hybrid 身份 · 只读 · 容器可达 · 工具进 Chat
RISK: 黄（IdP/网络；禁 0.0.0.0 公网裸 18090；禁 Agent 写库）
FAST: 否
仓：juanwan99/aivia-workbench
【硬门禁·回写】
  1) 填满 ops/C-REAL-RUNBOOK.md 并 push main
  2) EDU-BRIDGE 升 v0.2 · PIN 写 MODE=real|hybrid
  3) Issue #1 执行回写（网络方案 + Ce-R 摘要，无密钥）
  4) 缺一 → 禁止报完毕 · 禁止 CLAIM-C-REAL
【真源】CANON → PHASE-C-REAL-PACK → C-REAL-RUNBOOK
【做】C-R0…C-R6 · Ce-R0–R7 · smoke 扩展
      网络：host-gateway / 同网容器 / 内网反代 三选一
      edu 未就绪 → hybrid fixture，不得假 full real
【不做】CLAIM-B 冒充、公网匿名 exchange、直写 edu、重刷 B
【CLAIM】CLAIM-C-REAL 或 CLAIM-C-REAL(hybrid) · ≠ CLAIM-B
════════════════════════════════════
```

---

## 不必再开的卡

| 项 | 原因 |
|----|------|
| 重做 A/B/C-mock/C-FIX/D-LITE | 已收 |
| OpenWork 主线 | 二期 |
| 全校推广 | 绑 E1 + 授权 |

## 建议顺序

| 目标 | 先做 |
|------|------|
| 老师浏览器不报证书警告 | **卡 A E1** |
| Chat 里查本校班/课 | **卡 B C-REAL** |
| 两者都要 | E1 与 C-R0 可并行；C-R2 动网时保 G1 |
