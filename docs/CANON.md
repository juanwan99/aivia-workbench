# 正本 · CANON（唯一现行口径）

```
DOC: docs/CANON.md
DATE: 2026-08-06
STATUS: BINDING
UPDATED: CLAIM-D-LITE=YES（4会话空成功0·证据进仓）· E1后置 · CLAIM-B=NO · 正式上线=否
ONE_LINE: 可内测出件；不可正式上线；下一刀 E1 DNS-01 或 C-REAL
```


## 1. 现行真相

1. **Web** + **Dify 1.16.1** + **DeepSeek** + 现网。  
2. 默认入口：`/chat/lOMVPbz7rZmbJSJl`（**可内测**；自签警告已知）。  
3. A/B/Harden/DEBT 应用侧 **已收**。  
4. **E1 正式证书：后置**；CLAIM-B = **NO**。  
5. **阶段 C：** CLAIM-C 绿（MODE=mock）；**CLAIM-C-FIX 绿**（密钥强制 / smoke / systemd）。  
6. **阶段 D-LITE：** **CLAIM-D-LITE 绿**（≥3 会话 · 空成功 0 · 短报告）；**试点完成 ≠ 正式上线**。  
7. bridge：`127.0.0.1:18090` · **禁止公网裸奔**；AI 不直写 edu 库；本窗 **未接 edu real**。  
8. Dify 工具挂载：**书面后置**（容器够不到 loopback）。  
9. OpenWork 二期；密钥不进仓。  

## 2. 作废记忆

| 错误 | 状态 |
|------|------|
| C 完成 = 可对外正式上线 | **作废**（绑 E1） |
| D-LITE / 试点完成 = 正式上线 | **作废**（CLAIM-D-LITE ≠ CLAIM-B） |
| 弱 JWT 默认可上线 | **作废**（F1 拒绝启动） |
| Agent 写成绩 | **作废** |
| OpenWork 主线 | 作废 |

## 3. 优先级

1. CANON  
2. HANDOFF  
3. PHASE-D-PILOT-LITE-PACK · D-PILOT-RUNBOOK · D-PILOT-LITE-REPORT  
4. PHASE-C-FIX-DEPLOY-PACK · C-FIX-DEPLOY-RUNBOOK · PIN  
5. EDU-BRIDGE · PHASE-C-PACK  
