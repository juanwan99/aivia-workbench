# Aivia Workbench

学校 / 办公向 **浏览器公网 AI Agent 工作台**（任务 → 过程 → 可下载产物 → 停/重试 → 状态诚实）。

| 项 | 决策 |
|----|------|
| **产品形态** | **Web / 公网** |
| **主底座** | **[Dify](https://github.com/langgenius/dify)** 自托管 |
| **模型** | **DeepSeek** API |
| **部署** | 现网服务器 + 域名（见 `ops/INFRA.md`） |
| **入口** | **https://workbench.aivia.asia** |
| **业务** | edu-core 后置桥；AI 不直写业务库 |
| **正本** | [`docs/CANON.md`](./docs/CANON.md) |

## 一句话目标

> 打开域名 → 登录 → 下任务 → **有可下载产物** → 失败诚实。  
> **禁止空成功。**

## 用户成功

1. 浏览器打开工作台  
2. 登录 → 任务 → 过程可见  
3. 要 HTML/DOCX/PPTX 时能下载  
4. 能停、能再试；失败不假绿  

## 文档入口

| 文档 | 内容 |
|------|------|
| [docs/CANON.md](./docs/CANON.md) | 正本 |
| [docs/HANDOFF.md](./docs/HANDOFF.md) | 交接 |
| [ops/PHASE-A-CLOSEOUT.md](./ops/PHASE-A-CLOSEOUT.md) | **A 收口与残留风险** |
| [upstream/PIN.md](./upstream/PIN.md) | 版本钉 + A 验收 |
| [docs/PROJECT-PLAN.md](./docs/PROJECT-PLAN.md) | 阶段规划 |
| [docs/DELIVERY-RULES.md](./docs/DELIVERY-RULES.md) | B 交付纪律 |
| [ops/INSTALL.md](./ops/INSTALL.md) | 安装 |
| [ops/INFRA.md](./ops/INFRA.md) | 基建 |

## 二期（非主线）

OpenWork 桌面 = 本地增强可选。见 [ops/INSTALL-OPENWORK-optional.md](./ops/INSTALL-OPENWORK-optional.md)。

## 安全

- 禁止 API Key / 公网 IP / SSH 进仓  
- `.env` 仅服务器  

## 状态

| 项 | 状态 |
|----|------|
| 主线 | Dify Web + DeepSeek + 现网 |
| 阶段 A 功能（G0–G1+） | **已收** · 见 PIN |
| 入口硬化（正式证书 / 公网可达） | **进行中** · 见 CLOSEOUT |
| **下一刀** | 清 R-A1/R-A2 → **阶段 B**（10 次要课件空成功=0） |
