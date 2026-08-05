# 基础设施 · 服务器 / 域名

```
STATUS: BINDING · 2026-08-05
UPDATED: E1 正式证书仍 OPEN · 路径 = DNS-01
```

## 域名

| 主机 | 用途 |
|------|------|
| **workbench.aivia.asia** | Dify 主台 |
| pico.aivia.asia | 旧站过渡（冻结大功能） |

公网 IP / SSH **不进 Git**。

## 证书（E1）

| 项 | 状态 |
|----|------|
| 当前 | **自签** |
| HTTP-01 | **不可用**（外网 LE 403） |
| **必选** | **DNS-01** 或云厂商证书 |
| 执行包 | [`ops/PHASE-E1-PACK.md`](./PHASE-E1-PACK.md) |

## 禁止

无备份拆 Pico · 密钥/IP 进仓 · OpenWork 双主站
