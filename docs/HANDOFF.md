# HANDOFF · Aivia Workbench 总管交接

```
DOC: docs/HANDOFF.md
DATE: 2026-08-05
STATUS: BINDING · 新窗唯一入口（开场先读 docs/CANON.md）
UPDATED: 2026-08-05 · CLAIM-C 绿(mock) · E1 后置 · CLAIM-B 否
```

## 0. 怎么接

1. 读 CANON + 本文 + `ops/PHASE-C-PACK.md` + `ops/C-PATH-RUNBOOK.md` + `docs/EDU-BRIDGE.md`  
2. §5 打状态再干活  
3. 禁止：密钥进仓、自 PASS、OpenWork 主线、Agent 写 edu 库、E1 未满假正式上线  

## 1. 北极星

浏览器 → 任务 → **可一键下载产物** → 诚实状态。DeepSeek。对标 WorkBuddy 行为。  
C：带着 **学校身份** 干活；变更只走 **提案 + 人审**。

## 3.1 入口

| 项 | 状态 |
|----|------|
| 主站 | `https://workbench.aivia.asia` |
| **默认应用** | `https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl` |
| bridge | `http://127.0.0.1:18090/bridge/v1`（MODE=mock · PIN） |
| 证书 | **自签** · E1 **后置** |
| 配额 | max_active_requests=8 · nginx 30r/m/IP |

## 5. 状态报告模板

```text
【状态】Aivia Workbench 交接后首报
主仓: juanwan99/aivia-workbench
Pin: Dify 1.16.1 · deepseek-chat · bridge 0.1.0 mock
入口: /chat/lOMVPbz7rZmbJSJl
阶段: A/B/Harden/DEBT应用侧绿 | C 绿(mock) | E1 后置
CLAIM-C: YES (mock)
CLAIM-B: NO（E1 后置）
下一刀: 接 real edu 只读 或 E1 DNS-01
不做什么: Agent写库、假正式上线、OpenWork主线
```

## 6. 进度

| 项 | 状态 |
|----|------|
| A/B/Harden 应用 | 绿 |
| DEBT E2–E8 | 绿；E1 后置 |
| **C Ce 金路径** | **PASS** |
| CLAIM-B | **NO** |

## 11. 行动令

```text
1) 读 CANON + PHASE-C-PACK + C-PATH-RUNBOOK
2) bridge: bash bridge/run.sh （密钥 ~/.secrets/bridge.env）
3) 接真 edu 时改 MODE=real 并回归 Ce2–Ce5
4) E1 未过禁止教师正式上线话术
```
