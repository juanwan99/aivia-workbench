# HANDOFF · Aivia Workbench 总管交接

```
DOC: docs/HANDOFF.md
DATE: 2026-08-06
STATUS: BINDING
UPDATED: CLAIM-C-REAL(hybrid) · E1 BLOCKED · CLAIM-B NO
```

## 0. 怎么接

1. 读 CANON + 本文 + `ops/E1-RUNBOOK.md` + `ops/C-REAL-RUNBOOK.md`  
2. §5 打状态  
3. 禁止：密钥进仓、Agent 写库、公网匿名 exchange、假 CLAIM-B  

## 3.1 入口

| 项 | 状态 |
|----|------|
| 工作台 | `https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl`（自签） |
| bridge 主机 | `http://127.0.0.1:18090/bridge/v1` · hybrid 0.2.0 |
| bridge 容器 | `aivia-bridge` · dify_default |
| 烟测 | `bash bridge/smoke.sh` |
| 密钥 | `~/.secrets/bridge.env` |
| 证书 | **E1 BLOCKED** · 自签 |

## 5. 状态模板

```text
【状态】Aivia Workbench
Pin: Dify 1.16.1 · bridge 0.2.0 hybrid
CLAIM-C-REAL(hybrid): YES · E1: BLOCKED · CLAIM-B: NO · CLAIM-D-LITE: YES
下一刀: E1 DNS-01（业主）或 edu live 只读 → full real
正式上线: 否
```

## 11. 行动令

```text
桥: bash bridge/run.sh 或容器 aivia-bridge
验: curl 127.0.0.1:18090/bridge/v1/health
烟: bash bridge/smoke.sh
禁: 假 CLAIM-B / 密钥进 Git / 公网匿名 exchange
```
