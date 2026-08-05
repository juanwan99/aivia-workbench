# HANDOFF · Aivia Workbench 总管交接

```
DOC: docs/HANDOFF.md
DATE: 2026-08-06
STATUS: BINDING
UPDATED: CLAIM-D-LITE 绿 · E1 后置 · CLAIM-B 否 · 正式上线否
```

## 0. 怎么接

1. 读 CANON + 本文 + `ops/D-PILOT-LITE-REPORT.md` + `ops/C-FIX-DEPLOY-RUNBOOK.md`  
2. §5 打状态  
3. 禁止：密钥进仓、Agent 写库、公网裸 18090、CLAIM-B 未 E1、用试点话术冒充上线  

## 3.1 入口

| 项 | 状态 |
|----|------|
| 工作台 | `https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl` |
| 内测 | CLAIM-D-LITE · 自签警告已知 |
| bridge | `http://127.0.0.1:18090/bridge/v1` · v0.1.1 · MODE=mock |
| 守护 | `systemctl --user start aivia-bridge` |
| 烟测 | `bash bridge/smoke.sh` |
| 密钥 | `~/.secrets/bridge.env`（JWT + EXCHANGE_TOKEN） |
| 证书 | E1 后置 · 自签 |

## 5. 状态模板

```text
【状态】Aivia Workbench
Pin: Dify 1.16.1 · bridge 0.1.1 mock systemd
CLAIM-C: YES · CLAIM-C-FIX: YES · CLAIM-D-LITE: YES · CLAIM-B: NO
下一刀: E1 DNS-01（优先）或 PHASE-C-REAL
正式上线: 否
```

## 11. 行动令

```text
启: systemctl --user start aivia-bridge
验: curl 127.0.0.1:18090/bridge/v1/health
烟: bash bridge/smoke.sh
内测入口: /chat/lOMVPbz7rZmbJSJl
禁: 公网 18090 / secret 进 Git / 假 CLAIM-B / 全校推广话术
```
