# 阶段 C · 修复完善 + 部署包

```
STATUS: BINDING · CLAIM-C(mock) 审查后唯一执行包
DATE: 2026-08-06
CODE: PHASE-C-FIX-DEPLOY
对齐: PHASE-C-PACK · C-PATH-RUNBOOK · 深度审查债
前提: CLAIM-C YES (MODE=mock) · E1 后置 · CLAIM-B NO
出口: 部署可复活 + 密钥强制 + 烟测锁 401/403/apply + 真源无滞后
```

> **不重做 C 大叙事。** 只清审查债并完成可运维部署。  
> **不**因本包宣称 CLAIM-B 或 real edu 已通。

完整映射见历史审查债表；执行以 `ops/C-FIX-DEPLOY-RUNBOOK.md` 勾选为准。

## 完成定义（CLAIM-C-FIX）

```text
[ ] F0 真源无滞后
[ ] F1 无弱 secret 可启动；secret 仅服务器
[ ] F2 Dify 已挂工具 或 书面后置钉死
[ ] F3 smoke.sh 现网 PASS
[ ] D1 守护进程可复活
[ ] D2 暴露策略合规（默认本机）
[ ] D4 R1–R4
[ ] Issue 回写（无 Key）
[ ] 未勾 CLAIM-B；未假称 real edu
```

**本包绿 ≠ real edu。** real 另卡 `PHASE-C-REAL`。
