# 债务总账（唯一台账）

```
UPDATED: 2026-08-05
维护: 每清一项改本表 + PIN 一句
```

## 已关闭（勿再开大包）

| ID | 项 | 关闭证据 |
|----|-----|----------|
| A-* | 阶段 A 功能 G0–G1+ | PIN |
| B-battery | 10 次空成功 0 | B-PATH-RUNBOOK |
| H1/H3/H5/H7 | 应用硬化 | B-HARDEN-RUNBOOK |
| E0 | 治理扫尾 | CANON/HANDOFF |
| E2 | 并发+nginx 限流；日 token 书面后置 | DEBT-CLEAR-RUNBOOK |
| E3 | data-URL 正式；storage 书面后置 | 同上 |
| E4 | 教案永久 MD | skills + RUNBOOK |
| E5 | economy 永久 | RUNBOOK |
| E6 | 抽检目录 | RUNBOOK |
| E7 | Pico/备份记录；磁盘告警已记 | RUNBOOK |
| E8 | V1–V8 空成功 0 | RUNBOOK |
| R-A3 | G4 | B0/Harden/E8 |
| R-B6 | 双入口 | Agent site 关 |

## 开放（仅此）

| ID | 项 | 优先级 | 谁做 | 包 |
|----|-----|--------|------|-----|
| **E1 / R-A1 / R-B2** | 正式 HTTPS 无警告 | **P0** | 业主 DNS + 现网运维 | `ops/PHASE-E1-PACK.md` |
| **可达复核** | 证书后外网非 403、可聊可下 | **P0** | 同上 | E1 |
| 磁盘 84% | 清理/扩容计划 | P1 运维 | 现网 | Issue 记 |
| 日 token 账单级 | 后置 | P2 | 试点前 | 书面 |
| storage 附件 | 后置 | P2 | 可选 | — |
| DOCX / embedding | 后置 | P2 | 可选 | — |
| 阶段 C | edu 桥 | — | **须授权** | 另卡 |

## CLAIM

| CLAIM | 状态 |
|-------|------|
| 应用侧可用（内测） | YES |
| CLAIM-A 债务清零 | **NO** 直至 E1 |
| CLAIM-B 教师正式可用 | **NO** 直至 E1 |

**本台账结论：** 仓内/应用侧可清债务已清；**唯一阻塞 = E1 证书（DNS-01）**。
