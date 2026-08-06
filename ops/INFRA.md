# 基础设施 · 服务器 / 域名 / IP

```
STATUS: BINDING · 2026-08-06
对齐: E1-RUNBOOK · QUAD-LAUNCH
UPDATED: 公网入口 asyncova.com 边缘；源站 workbench LE 保留（ICP 债）
```

## 1. 业主口径

沿用现有服务器与域名体系；**公网主入口为海外边缘 `asyncova.com`**（规避 aivia.asia 未备案拦截）。

## 2. 域名

| 主机名 | 用途 | 状态 |
|--------|------|------|
| **`asyncova.com`** | **公网主入口**（Chat/experts/dl） | **LE YE2 · 海外** |
| **`workbench.aivia.asia`** | 源站 Dify/bridge | **LE YE2 · 大陆 EIP ICP 拦** |
| `pico.aivia.asia` | 旧站过渡 | 保留 |

> 公网 IP / SSH / AK **不进 Git**。

## 3. 证书与可达

| 项 | 状态 |
|----|------|
| 公网 HTTPS | **asyncova.com** Let's Encrypt YE2 |
| 源站 HTTPS | workbench LE YE2 · 机房内 VERIFY_OK |
| 源站路径 | `/etc/letsencrypt/live/workbench.aivia.asia/` |
| 边缘反代 | dmit nginx → SSH 隧道 → ECS `:13080` |
| 续期 | 源站 acme.sh DNS-01；边缘 certbot webroot |
| ICP | `*.aivia.asia` 大陆拦截未解 |

## 4. bridge

| 项 | 值 |
|----|-----|
| 版本/MODE | **0.2.2 / hybrid** |
| 容器 | `aivia-bridge` · `dify_default` |
| PUBLIC_DL | `https://asyncova.com/dl` |
| 禁止 | 公网匿名 exchange · 假 full real |

## 5. 禁止

- 密钥 / AK / 私钥进仓  
- HTTP-01 死磕  
- E1 未过假 CLAIM-B（现 E1 已过，CLAIM-B 仍需产品门禁）  
