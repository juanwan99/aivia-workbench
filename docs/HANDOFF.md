# HANDOFF · Aivia Workbench 总管交接

```
DOC: docs/HANDOFF.md
DATE: 2026-08-05
STATUS: BINDING · 新窗唯一入口（开场先读 docs/CANON.md）
UPDATED: 2026-08-05 · A 绿 · B 电池有条件绿 · B-HARDEN 应用侧绿 · H2 证书仍 OPEN
```

## 0. 怎么接

1. 读 CANON + 本文 + `ops/PHASE-B-CLOSEOUT.md` + `ops/B-HARDEN-RUNBOOK.md`  
2. §5 打状态再干活  
3. 禁止：密钥进仓、自 PASS、OpenWork 主线、未授权 C、H2 未满假正式上线  

## 1. 北极星

浏览器 → 任务 → **可一键下载产物** → 诚实状态。DeepSeek。对标 WorkBuddy 行为。

## 3.1 入口

| 项 | 状态 |
|----|------|
| 主站 | `https://workbench.aivia.asia` |
| **默认应用（唯一主推）** | `https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl` |
| 旧 Agent 公开站 | **已关闭** enable_site=false |
| 证书 | **自签** → 下一刀 H2 DNS-01/云证书 |
| 配额 | max_active_requests=8 · nginx 30r/m/IP |

## 5. 状态报告模板

```text
【状态】Aivia Workbench 交接后首报
主仓: juanwan99/aivia-workbench
Pin: Dify 1.16.1 · deepseek-chat
入口: /chat/lOMVPbz7rZmbJSJl
阶段: A 功能绿 | B 电池空成功0 | Harden 应用绿(H1/H3/H7) | H2 证书 OPEN
下一刀: 正式 HTTPS（DNS-01）或授权后 C
不做什么: 重刷B、OpenWork主线、未授权C、假正式上线
```

## 6. 进度

| 项 | 状态 |
|----|------|
| A G0–G1+ | PASS |
| B 10 次空成功 0 | PASS（有条件 M3） |
| H1 真下载 | **PASS** |
| H2 证书 | **OPEN / 范围限制** |
| H3 配额 | **PASS**（并发+nginx） |
| H7 回归 | **空成功 0** |
| C edu | 须授权 |

## 11. 行动令

```text
1) 读 CANON + B-CLOSEOUT + B-HARDEN-RUNBOOK
2) 优先 H2 正式证书，再谈教师正式使用
3) C 须业主授权
```
