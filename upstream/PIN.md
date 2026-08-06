# 上游版本钉扎

```
STATUS: CLAIM-QUAD-FIX-DEPLOY=YES · CLAIM-QUAD-LAUNCH=YES · FULL-REAL=NO · 正式上线=是（受限） · bridge=0.2.2
DATE: 2026-08-06
ONE_LINE: CLAIM-QUAD-FIX-DEPLOY=YES（/experts 双路径无:8443 · 隧道 systemd 可 restart）；FULL-REAL=NO
```

| 组件 | 版本 | 日期 | 备注 |
|------|------|------|------|
| **Dify** | `1.16.1` | 2026-08-05 | Chat `lOMVPbz7rZmbJSJl` |
| **workflow** | fix-deploy | 2026-08-06 | |
| **TLS 公网** | asyncova.com LE | 2026-08-06 | 边缘 |
| **bridge** | 0.2.2 hybrid | 2026-08-06 | PUBLIC_DL=asyncova.com/dl |
| **隧道** | user systemd | 2026-08-06 | aivia-edge-tunnel · 无 User= |
| **专家** | /experts 双路径 | 2026-08-06 | 无 :8443 跳转 |
| **QUAD-FIX-DEPLOY** | **PASS** | 2026-08-06 | **CLAIM-QUAD-FIX-DEPLOY=YES** |

> 公网主入口：`https://asyncova.com`  
> 专家：`https://asyncova.com/experts`（有无斜杠均可）  
> 下载：`https://asyncova.com/dl/{id}/file.{ext}`

## 出口

| 项 | 结果 |
|----|------|
| **CLAIM-QUAD-FIX-DEPLOY** | **YES** |
| F1+F2 | **硬绿** |
| FULL-REAL | **NO** |
| 正式上线 | **是（受限）** · 未扩大 |
| 证据 | `ops/evidence/quad-fix-deploy/` |
