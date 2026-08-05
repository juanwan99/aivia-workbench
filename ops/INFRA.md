# 基础设施 · 服务器 / 域名 / IP

```
STATUS: BINDING · 2026-08-05
对齐: docs/HANDOFF.md §3.1 · D9
UPDATED: 主入口 workbench 已挂 Dify；正式证书与 WAF 仍 OPEN
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

## 4. 证书与可达（残留）

| 项 | 状态 |
|----|------|
| HTTPS | **临时自签** → 待正式证书（DNS-01 或平台证书） |
| 外网探测 | 可能遇 WAF **403** → 须放行 Host 与健康检查 |
| 验收 | 浏览器**无证书警告**且能登录、能打开课件应用 |

详见 [`ops/PHASE-A-CLOSEOUT.md`](./PHASE-A-CLOSEOUT.md) R-A1 / R-A2。

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
