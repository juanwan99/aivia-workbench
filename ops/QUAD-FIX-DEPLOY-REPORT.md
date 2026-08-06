# QUAD-FIX-DEPLOY 报告

```
DATE: 2026-08-06
PHASE-QUAD-FIX-DEPLOY: PASS
CLAIM-QUAD-FIX-DEPLOY: YES
正式上线: 是（受限）· 未扩大
FULL-REAL: NO
空成功: 0
```

## 1. 结论

修通 QUAD-LAUNCH 条件绿遗留：**专家台无斜杠可开且不跳 :8443**；**边缘隧道 systemd 可 restart 回归**。可报 **CLAIM-QUAD-FIX-DEPLOY=YES**（F1+F2 硬绿）。

## 2. F1 / X1 nginx

| 路径 | 结果 |
|------|------|
| `GET https://asyncova.com/experts` | **200** · X-Aivia-Experts-Path: exact |
| `GET https://asyncova.com/experts/` | **200** · slash |
| Location 含 `:8443` | **无** |

根因：8443 上相对 302 带端口。处置：双路径 `alias` 直出，取消 302。

## 3. F2 / X2 隧道

| 项 | 结果 |
|----|------|
| unit | user `aivia-edge-tunnel.service` |
| 根因 216 | user unit 写了 `User=ops` |
| active | **running** |
| restart 回归 | **tunnel=200** |

## 4. X3 / X4

- catalog：`ops/evidence/quad-fix-deploy/experts/catalog.yaml`
- NOTES 回滚：`ops/QUAD-FIX-DEPLOY-NOTES.md`
- Chat `/chat/lOMVPbz7rZmbJSJl` 200 · `/dl` attachment 200

## 5. 证据

`ops/evidence/quad-fix-deploy/`：gate-X* · f1-experts-public.txt · f2-tunnel-status.txt · x4-dl.txt · edge/*

## 6. 限制（未变）

- FULL-REAL=NO · 正式上线仍「受限」· ≠ 全校  
- 公网主入口仍 asyncova.com · aivia.asia ICP 债仍在  
- 无密钥进仓  

## 7. CLAIM

```text
CLAIM-QUAD-FIX-DEPLOY: YES
= F1 专家双路径硬绿 + F2 隧道 systemd 硬绿 + 文档/回归
≠ 假 full real · ≠ 扩大全校
```
