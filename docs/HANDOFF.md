# HANDOFF · Aivia Workbench 总管交接

```
DOC: docs/HANDOFF.md
DATE: 2026-08-06
STATUS: BINDING
UPDATED: P0-GATE PASS · CLAIM-B=YES · 正式上线=否
```

## 0. 怎么接

1. 读 CANON + 本文 + `ops/P0-GATE-REPORT.md` + `ops/CLAIM-B-SCRIPT.md`  
2. §5 打状态  
3. 禁止：密钥进仓、Agent 写库、假全校上线、空成功报绿  

## 3.1 入口

| 项 | 状态 |
|----|------|
| 工作台 | `https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl` |
| 证书 | LE YE2 · 应无浏览器警告 |
| CLAIM-B | **YES**（教师可用默认链） |
| 正式上线 | **否** |
| bridge | hybrid 0.2.0 · `127.0.0.1:18090` + 容器 `aivia-bridge` |

## 5. 状态模板

```text
【状态】Aivia Workbench
Pin: Dify 1.16.1 · bridge 0.2.0 hybrid · TLS LE YE2
P0-GATE: PASS · CLAIM-B: YES · 正式上线: 否 · full real: 跳过
下一刀: 4G 人眼确认 / edu live 只读 / dns_ali 续期
```

## 11. 行动令

```text
入口: 默认 Chat 链
话术: ops/CLAIM-B-SCRIPT.md
烟: bash bridge/smoke.sh
禁: 全校推广未授权 · 密钥进 Git · Agent 写库
```
