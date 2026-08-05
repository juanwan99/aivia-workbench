# 阶段 B 收口纪要 · 有条件关闭 + Harden

```
DATE: 2026-08-05
STATUS: 纪律电池有条件绿 · 应用硬化绿 · 对外入口仍受限
证据: upstream/PIN.md · ops/B-PATH-RUNBOOK.md · ops/B-HARDEN-RUNBOOK.md · Issue #1
审查: M3 纪律有条件 · Harden H1/H3/H7 绿 · H2 未满不得教师正式上线
```

## 1. 已确认完成

| 项 | 证据 |
|----|------|
| 10 次电池空成功 = 0 | B-PATH-RUNBOOK |
| H1 真下载（data-URL 控件） | Harden Chatflow Code 节点 · R1/R2/R5 |
| H3 并发/限流 | max_active_requests=8 · nginx 30r/m/IP |
| H4 教案 scope | **MD only** 书面 |
| H5 单入口 | 仅推 lOMVPbz7rZmbJSJl · Agent 公开站关闭 |
| H7 五次回归空成功 0 | B-HARDEN-RUNBOOK |
| G4 / R4 不假绿 | 明确失败人话 |

## 2. 残留（Harden 后）

| ID | 状态 |
|----|------|
| R-B1 代码块 vs 附件 | **已改善** → data-URL 一键下载（非平台 storage 附件，但满足「真下载控件」） |
| R-B2 自签证书 | **OPEN** · 需 DNS-01/云证书 |
| R-B3 公网 403 | **观察** · 自签下可打开；WAF 对 LE 校验仍可能 403 |
| R-B4 真配额 | **已改善** · 并发+nginx 限流；账单级日 token 可后置 |
| R-B5 教案 DOCX | **书面后置** · v0.x=MD |
| R-B6 双入口 | **关闭** · Agent enable_site=false |
| R-B8 真源过时 | **本次同步** |

## 3. 默认入口

`https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl`

## 4. 下一刀

- **H2 正式证书**（DNS-01 或云厂商）后方可谈教师正式使用  
- 阶段 C edu 桥：**另授权**  
- 可选：平台 storage 附件出件、DOCX 转换、embedding 知识库加强  
