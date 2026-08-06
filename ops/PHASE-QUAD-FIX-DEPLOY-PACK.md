# 任务包 · PHASE-QUAD-FIX-DEPLOY

```
STATUS: DONE · CLAIM-QUAD-FIX-DEPLOY=YES
DATE: 2026-08-06
CODE: PHASE-QUAD-FIX-DEPLOY
前提: CLAIM-QUAD-LAUNCH=YES · 正式上线=是（受限）· FULL-REAL=NO
模式: X0→X4 自审→修→过门
```

## 完成定义

```text
CLAIM-QUAD-FIX-DEPLOY 当且仅当：
  [x] F1/X1：/experts 与 /experts/ 均 200 · 响应无 :8443
  [x] F2/X2：systemd 隧道 active · restart 后 probe 200
  [x] X3：catalog.yaml + QUAD-FIX-DEPLOY-NOTES（含回滚）
  [x] X4：Chat + /dl 回归 · 无斜杠专家台 · PIN/Issue
  [x] evidence/quad-fix-deploy gates · 空成功 0 · 无密钥
禁止：假 full real · 扩大全校 · 只写文档不修入口
```

## 阶段

| 阶段 | 内容 |
|------|------|
| X0 | 基线：确认 302→:8443 与 216/GROUP |
| X1 | nginx 双路径直出 |
| X2 | user unit 去 User= · restart 回归 |
| X3 | catalog + NOTES |
| X4 | 回归 + 真源回写 |
