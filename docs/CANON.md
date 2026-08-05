# 正本 · CANON（唯一现行口径）

```
DOC: docs/CANON.md
DATE: 2026-08-06
STATUS: BINDING
UPDATED: CLAIM-C-REAL(hybrid)=YES · E1=BLOCKED · CLAIM-B=NO · 正式上线=否
ONE_LINE: hybrid 桥+工具可测；证书仍自签；不可正式上线；下一刀 E1 DNS-01
```

## 1. 现行真相

1. **Web** + **Dify 1.16.1** + **DeepSeek** + 现网。  
2. 默认入口：`/chat/lOMVPbz7rZmbJSJl`（内测；**自签警告仍在**）。  
3. A/B/Harden/DEBT 应用侧 **已收**；**CLAIM-D-LITE 绿**。  
4. **E1 正式证书：BLOCKED**（无 DNS-01 能力/无 root 写证/certbot 破损）→ **CLAIM-B = NO**。  
5. **阶段 C：** CLAIM-C + CLAIM-C-FIX 绿；**CLAIM-C-REAL(hybrid) 绿**（fixture + 容器可达 + Dify 工具命中）。  
6. **非** CLAIM-C-REAL full（edu-core 业务只读 API 未挂）。  
7. bridge：**0.2.0** · MODE=**hybrid** · 主机 + `aivia-bridge` 容器；**禁止**公网匿名 exchange。  
8. OpenWork 二期；密钥不进仓。  

## 2. 作废记忆

| 错误 | 状态 |
|------|------|
| hybrid = full real / 可对外正式上线 | **作废**（绑 E1 + live edu） |
| E1 未过勾 CLAIM-B | **作废** |
| Agent 写成绩 | **作废** |
| OpenWork 主线 | 作废 |

## 3. 优先级

1. CANON  
2. HANDOFF  
3. PHASE-E1-PACK · E1-RUNBOOK · PHASE-C-REAL-PACK · C-REAL-RUNBOOK  
4. EDU-BRIDGE v0.2 · PIN · INFRA  
