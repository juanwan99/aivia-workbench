# C 修复完善 + 部署 · 勾选清单

日期：2026-08-06    执行人：phase-c-fix-deploy（ECS）  
bridge：`http://127.0.0.1:18090/bridge/v1`  
版本：**0.1.1**  
守护：**systemd --user aivia-bridge**

正文：`ops/PHASE-C-FIX-DEPLOY-PACK.md`

## F0 真源

- [x] DEBT-LEDGER / CANON / HANDOFF 指向 FIX-DEPLOY  
- **结果：** **PASS**  

## F1 密钥

- [x] 无 secret / 弱 secret 启动失败  
- [x] 有 secret health 200  
- [x] `BRIDGE_EXCHANGE_TOKEN` 已设；错误 token exchange **401**  
- **结果：** **PASS**  

## F2 Dify

- [ ] 路径甲：工具已挂  
- [x] **路径乙：书面后置** — C mock 以 API/Ce/smoke 为准；Dify 容器够不到 loopback:18090，挂载后置 real/专网（**勿** 0.0.0.0 公网）  
- **结果：** **DEFER（书面）**  

## F3 烟测

- [x] `bash bridge/smoke.sh` 退出 0（11/11）  
- **结果：** **PASS**  

## F4 小清理

- [x] openapi servers → `http://127.0.0.1:18090/bridge/v1`  
- [x] audit 默认本校过滤  
- [x] 版本 **0.1.1**  
- **结果：** **PASS**  

## D1 守护

- [x] systemd user：`aivia-bridge.service`  
- [x] kill 后 **Restart=always** → 新 PID + health 200  

- **结果：** **PASS**  

## D2 暴露

- [x] 默认 `BRIDGE_HOST=127.0.0.1`  
- [x] 无公网裸 18090（ss 仅 loopback）  
- **结果：** **PASS**  

## D4 回归

| ID | 结果 |
|----|------|
| R1 smoke | **PASS** |
| R2 G1 | **PASS** |
| R3 跨校 403 | **PASS**（smoke） |
| R4 PIN | **PASS** |

## CLAIM-C-FIX

- [x] 可报修复部署绿  
- [x] 未勾 CLAIM-B  
- [x] 未勾 real edu  

```text
摘要：2026-08-06 / systemd-user aivia-bridge / Dify挂载=书面后置 / smoke 11ok / v0.1.1
CLAIM-C-FIX: YES
CLAIM-B: NO
MODE: mock
```
