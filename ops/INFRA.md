# 基础设施 · 服务器 / 域名 / IP

```
STATUS: BINDING · 2026-08-05
对齐: docs/HANDOFF.md §3.1 · DEBT-CLEAR E1
UPDATED: 主入口 workbench 已挂 Dify；正式证书 E1 BLOCKED（HTTP-01 外网失败 → DNS-01）
```

## 1. 业主口径

**沿用现有服务器、公网 IP 与 `aivia.asia` 域名体系。** 不强制新购机器。

## 2. 角色分工

| 层级 | 跑什么 |
|------|--------|
| **现有服务器** | **Dify Docker = 主入口**；过渡 Pico；日后 edu 桥 |
| **用户浏览器** | **https://workbench.aivia.asia** |
| **本机（二期）** | 可选 OpenWork，不占主入口 |

## 3. 域名（现行）

| 主机名 | 用途 | 状态 |
|--------|------|------|
| `pico.aivia.asia` | 旧站过渡 | 保留；大功能冻结 |
| **`workbench.aivia.asia`** | **Dify Web 主台** | **已指向现网反代**（本机 `127.0.0.1:13080`） |
| 根域 `aivia.asia` | 品牌跳转 | 按需 |

用 Caddy/Nginx/Traefik **按 Host 分流**。

> **具体公网 IP、SSH、面板账号：不进 Git。** 运维私密持有。  
> 曾误写入 PIN 的 IP 明文已在收口时清除。

## 4. 证书与可达（E1）

| 项 | 状态 |
|----|------|
| HTTPS | **临时自签**（`/etc/letsencrypt/live/workbench.aivia.asia/` 现为自签占位） |
| HTTP-01 | **失败**：本机 ACME webroot 有 body；**外网 LE 校验 403/空 body**（路径级阻断） |
| DNS-01 | **必选路径**：阿里云 DNS（NS=`dns1/2.hichina.com`）+ certbot manual/dns 插件 |
| 站点可达 | 公网 HTTPS **200**（自签警告下可聊可下载） |
| 验收 E1 | 浏览器**无证书警告** + 默认 Chat 可开 |

详见 [`ops/PHASE-DEBT-CLEAR-PACK.md`](./PHASE-DEBT-CLEAR-PACK.md) E1 · [`ops/DEBT-CLEAR-RUNBOOK.md`](./DEBT-CLEAR-RUNBOOK.md)。

## 5. 阶段依赖

| 阶段 | 基建 |
|------|------|
| A 功能 | 子域 + Docker 已满足 |
| A 产品可用 | **正式 HTTPS + 公网可达** |
| B | 同主入口 |
| C edu | HTTPS 子域稳定 |

## 6. 禁止

- 无备份拆 Pico 域名  
- 密钥 / IP / SSH 进仓库  
- OpenWork 与 Dify 双主站  

## 7. 回写

入口或证书状态变化 → 更新本节 + HANDOFF §3.1 + Issue #1 一句。

## 8. bridge（阶段 C）

| 项 | 值 |
|----|----|
| 监听 | `127.0.0.1:18090` 仅本机 |
| 守护 | `systemctl --user enable --now aivia-bridge` |
| 健康 | `curl -sS http://127.0.0.1:18090/bridge/v1/health` |
| 烟测 | `bash bridge/smoke.sh` |
| 密钥 | `~/.secrets/bridge.env`（不进 Git） |
| 禁止 | 公网裸映射 18090 / 匿名 exchange |

