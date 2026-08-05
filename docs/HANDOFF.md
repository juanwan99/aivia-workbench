# HANDOFF · Aivia Workbench 总管交接

```
DOC: docs/HANDOFF.md
DATE: 2026-08-05
STATUS: BINDING · 新窗唯一入口（开场先读 docs/CANON.md）
UPDATED: 2026-08-05 · DEBT-CLEAR 应用侧收口 · E1 证书 BLOCKED
```

## 0. 怎么接

1. 读 CANON + 本文 + `ops/PHASE-DEBT-CLEAR-PACK.md` + `ops/DEBT-CLEAR-RUNBOOK.md`  
2. §5 打状态再干活  
3. 禁止：密钥进仓、自 PASS、OpenWork 主线、未授权 C、E1 未满假正式上线  

## 1. 北极星

浏览器 → 任务 → **可一键下载产物** → 诚实状态。DeepSeek。对标 WorkBuddy 行为。

## 3.1 入口

| 项 | 状态 |
|----|------|
| 主站 | `https://workbench.aivia.asia` |
| **默认应用（唯一主推）** | `https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl` |
| 旧 Agent 公开站 | **已关闭** enable_site=false |
| 证书 | **自签** · E1 **BLOCKED**（外网 HTTP-01 失败 → 需 DNS-01/云证书） |
| 配额 | max_active_requests=8 · nginx 30r/m/IP · 日 token 账单级后置 |

## 5. 状态报告模板

```text
【状态】Aivia Workbench 交接后首报
主仓: juanwan99/aivia-workbench
Pin: Dify 1.16.1 · deepseek-chat
入口: /chat/lOMVPbz7rZmbJSJl
阶段: A 功能绿 | B 空成功0 | Harden 应用绿 | DEBT-CLEAR 应用侧 E2–E8 | E1 证书 BLOCKED
CLAIM-A: NO（E1 未满）
CLAIM-B: NO（E1 未满）
下一刀: DNS-01 正式证书（阿里云 DNS API 或手工 TXT）
不做什么: 重刷B、OpenWork主线、未授权C、假正式上线
```

## 6. 进度

| 项 | 状态 |
|----|------|
| A G0–G1+ | PASS |
| B 10 次空成功 0 | PASS（有条件 M3） |
| H1 真下载 | **PASS**（data-URL） |
| H3 配额 | **PASS** |
| H7 回归 | **空成功 0** |
| **E1 证书** | **BLOCKED** |
| E2–E5 / E7 | **PASS**（书面后置项见 RUNBOOK） |
| **E8 V1–V8** | **空成功 0** |
| C edu | 须授权 |

## 11. 行动令

```text
1) 读 CANON + PHASE-DEBT-CLEAR-PACK + DEBT-CLEAR-RUNBOOK
2) 优先 E1：DNS-01 正式证书（HTTP-01 现网不可用）
3) E1 满前禁止教师正式使用话术
4) C 须业主授权
```
