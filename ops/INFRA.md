# 基础设施 · 服务器 / 域名 / IP

```
STATUS: BINDING · 2026-08-06
对齐: docs/HANDOFF.md · E1-RUNBOOK · C-REAL-RUNBOOK
UPDATED: E1 BLOCKED（仍自签）· bridge hybrid 容器进 dify_default · SSRF 白名单 aivia-bridge
```

## 1. 业主口径

**沿用现有服务器、公网 IP 与 `aivia.asia` 域名体系。** 不强制新购机器。

## 2. 角色分工

| 层级 | 跑什么 |
|------|--------|
| **现有服务器** | **Dify Docker = 主入口**；bridge；过渡 Pico |
| **用户浏览器** | **https://workbench.aivia.asia**（自签警告直至 E1） |
| **本机（二期）** | 可选 OpenWork，不占主入口 |

## 3. 域名（现行）

| 主机名 | 用途 | 状态 |
|--------|------|------|
| `pico.aivia.asia` | 旧站过渡 | 保留 |
| **`workbench.aivia.asia`** | **Dify Web 主台** | 反代 → `127.0.0.1:13080` |
| 根域 `aivia.asia` | 品牌跳转 | 按需 |

> **具体公网 IP、SSH、面板账号：不进 Git。**

## 4. 证书与可达（E1）

| 项 | 状态 |
|----|------|
| HTTPS | **临时自签**（`/etc/letsencrypt/live/workbench.aivia.asia/`） |
| HTTP-01 | **放弃死磕**（外网 LE 历史 403） |
| DNS-01 | **必选**：阿里云 DNS（NS=hichina）+ 业主 AK/手工 TXT/云证书 |
| 本窗 | **E1 BLOCKED**（无 DNS 能力 + 无 root 写证 + certbot 破损） |
| 验收 E1 | 浏览器**无证书警告** + Chat 可开 + 外网/4G |

详见 `ops/E1-RUNBOOK.md`。

## 5. bridge（C-REAL hybrid）

| 项 | 值 |
|----|-----|
| 版本/MODE | **0.2.0 / hybrid** |
| 主机 | 运维 smoke · exchange token 强制 |
| 容器 | **`aivia-bridge`** · 网络 `dify_default` |
| Dify 工具 URL | 容器名或容器 IP `:18090/bridge/v1` |
| SSRF | `SSRF_PROXY_ALLOW_PRIVATE_DOMAINS=aivia-bridge` + bridge IP（docker `.env`） |
| 密钥 | `~/.secrets/bridge.env`（不进 Git） |
| 禁止 | 公网匿名 exchange · Agent 写 edu |

## 6. 禁止

- 无备份拆 Pico 域名  
- 密钥 / IP / SSH 进仓库  
- OpenWork 与 Dify 双主站  
- E1 未过宣称 CLAIM-B  

## 7. 回写

证书或 bridge 网络变化 → 更新本节 + HANDOFF + PIN + Issue。
