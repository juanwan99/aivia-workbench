# C 修复完善 + 部署 · 勾选清单

日期：________    执行人：________  
bridge：`http://127.0.0.1:18090/bridge/v1`  
版本：________  

正文：`ops/PHASE-C-FIX-DEPLOY-PACK.md`

## F0 真源

- [ ] DEBT-LEDGER / CANON / HANDOFF 指向 FIX-DEPLOY  
- **结果：** PASS / FAIL  

## F1 密钥

- [ ] 无 secret 启动失败  
- [ ] 有 secret health 200  
- [ ] （可选）EXCHANGE_TOKEN 已设  
- **结果：** PASS / FAIL  

## F2 Dify

- [ ] 路径甲：工具已挂 · 应用名：________  
- [ ] 或路径乙：书面后置 Issue  
- **结果：** PASS / DEFER  

## F3 烟测

- [ ] `bash bridge/smoke.sh` 退出 0  
- **结果：** PASS / FAIL  

## F4 小清理

- [ ] openapi servers  
- [ ] audit 过滤（若做）  
- **结果：** PASS / SKIP  

## D1 守护

- [ ] systemd / compose（圈一）：________  
- [ ] 重启后 health 仍 200  
- **结果：** PASS / FAIL  

## D2 暴露

- [ ] 默认 127.0.0.1  
- [ ] 无公网裸 18090  
- **结果：** PASS / FAIL  

## D4 回归

| ID | 结果 |
|----|------|
| R1 smoke | |
| R2 G1 | |
| R3 跨校 403 | |
| R4 PIN | |

## CLAIM-C-FIX

- [ ] 可报修复部署绿  
- [ ] 未勾 CLAIM-B  
- [ ] 未勾 real edu  

```text
摘要：日期 / 守护方式 / Dify挂载是否 / smoke / 备注
```
