# 基础设施 · 服务器 / 域名 / IP

```
STATUS: BINDING · 2026-08-06
对齐: E1-RUNBOOK · C-REAL-RUNBOOK
UPDATED: E1 PASS — Let's Encrypt YE2 via DNS-01 (acme.sh manual)
```

## 1. 业主口径

沿用现有服务器与 `aivia.asia` 域名体系。

## 2. 域名

| 主机名 | 用途 | 状态 |
|--------|------|------|
| **`workbench.aivia.asia`** | Dify Web 主台 | **正式 HTTPS（LE）** |
| `pico.aivia.asia` | 旧站过渡 | 保留 |

> 公网 IP / SSH / AK **不进 Git**。

## 3. 证书与可达（E1）

| 项 | 状态 |
|----|------|
| HTTPS | **Let's Encrypt YE2** |
| 路径 | `/etc/letsencrypt/live/workbench.aivia.asia/` |
| 签发 | acme.sh DNS-01 手工 + 业主阿里云 TXT |
| 续期 | 建议改 `dns_ali` 自动；手工模式每次需新 TXT |
| ACME 客户端 | `~/.acme.sh`（ops） |
| 自签备份 | `/tmp/e1-cert-backup/*.bak-selfsign` |

## 4. bridge

| 项 | 值 |
|----|-----|
| 版本/MODE | 0.2.0 / hybrid |
| 容器 | `aivia-bridge` · `dify_default` |
| 禁止 | 公网匿名 exchange |

## 5. 禁止

- 密钥 / AK / 私钥进仓  
- HTTP-01 死磕  
- E1 未过假 CLAIM-B（现 E1 已过，CLAIM-B 仍需产品门禁）  
