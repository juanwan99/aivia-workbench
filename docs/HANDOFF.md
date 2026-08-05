# HANDOFF · Aivia Workbench 总管交接

```
DOC: docs/HANDOFF.md
DATE: 2026-08-05
STATUS: BINDING
UPDATED: 下一刀 = 仅 E1（DNS-01 正式证书）· 应用债已清
```

## 0. 怎么接

1. 读 CANON + `ops/DEBT-LEDGER.md` + `ops/PHASE-E1-PACK.md`  
2. §5 状态  
3. 禁止：假上线、未授权 C、重刷 B、密钥进仓  

## 1. 北极星

浏览器 → 任务 → 可下载产物 → 诚实状态。

## 3.1 入口

| 项 | 状态 |
|----|------|
| 默认 Chat | `https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl` |
| 证书 | **自签 · E1 OPEN** |
| 应用侧 | 绿（可内测） |

## 5. 状态模板

```text
【状态】Aivia Workbench
Pin: Dify 1.16.1 · deepseek-chat
入口: /chat/lOMVPbz7rZmbJSJl
已清: A/B/Harden/DEBT 应用侧（见 DEBT-LEDGER）
阻塞: E1 正式证书 DNS-01
下一刀: ops/PHASE-E1-PACK.md
CLAIM-A/B: NO
不做: C 未授权、重刷B、假上线
```

## 11. 行动令

```text
1) 仅执行 PHASE-E1-PACK / E1-RUNBOOK
2) 业主阿里云 DNS TXT 或 DNS RAM
3) E1 PASS 后更新 DEBT-LEDGER + PIN + Issue
4) C 另授权
```
