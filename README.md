# Aivia Workbench

学校 / 办公向 **浏览器公网 AI Agent 工作台**（任务 → 过程 → 可下载产物 → 停/重试 → 状态诚实）。

| 项 | 决策 |
|----|------|
| **产品形态** | **Web / 公网**（人在浏览器里下任务） |
| **主底座** | **[Dify](https://github.com/langgenius/dify)**（自托管 Docker） |
| **模型** | **DeepSeek** API（默认） |
| **部署** | **云端优先**：挂**现有服务器 + 域名/IP**（见 `ops/INFRA.md`） |
| **业务真源** | edu-core（后置身份桥；AI **不**直写业务库） |
| **体验对标** | WorkBuddy **响应逻辑**（clean-room，不抄闭源） |
| **旧仓** | `juanwan99/pico` 大功能冻结；本仓为新主线 |
| **正本** | [`docs/CANON.md`](./docs/CANON.md)（作废错误记忆） |

## 一句话目标

> 打开域名 → 登录 → 下任务 → Agent/工作流真执行 → **有可下载产物** → 失败诚实可再试。  
> **禁止「终态成功但无文件」。**

## 用户成功（产品尺子）

1. 浏览器打开工作台 URL（子域或现网入口）  
2. 能登录  
3. 能下任务，过程可见  
4. 要 HTML / DOCX / PPTX 时，**能下载到真文件**  
5. 能停、能再试；失败不假绿  

## 仓库结构

```text
docs/                 规划、CANON、架构、选型、金路径、交付纪律
ops/                  现网安装、基建、DeepSeek 样例（无密钥）
upstream/             上游版本钉（Dify 为主）
skills/               课件/教案类提示与工作流资产（阶段 B）
bridge/               edu JWT / 身份桥（后置）
```

## 文档入口

| 文档 | 内容 |
|------|------|
| [docs/CANON.md](./docs/CANON.md) | **正本清源（先读）** |
| [docs/HANDOFF.md](./docs/HANDOFF.md) | 总管交接 |
| [docs/PROJECT-PLAN.md](./docs/PROJECT-PLAN.md) | 阶段 A–D |
| [docs/SELECTION-WEB-v2.md](./docs/SELECTION-WEB-v2.md) | 选型结论 |
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | 分层（Dify 主台） |
| [docs/CHANGE-POLICY.md](./docs/CHANGE-POLICY.md) | 改 / 不改 |
| [docs/GOLD-PATHS.md](./docs/GOLD-PATHS.md) | **浏览器**金路径 |
| [docs/DELIVERY-RULES.md](./docs/DELIVERY-RULES.md) | 交付硬规则 |
| [ops/INSTALL.md](./ops/INSTALL.md) | **现网 Dify + DeepSeek** |
| [ops/INFRA.md](./ops/INFRA.md) | 服务器 / 域名 / IP |

## 二期 · 非主线（可选）

**OpenWork**（桌面）仅为 **本地文件增强**，不占主入口。见 [ops/INSTALL-OPENWORK-optional.md](./ops/INSTALL-OPENWORK-optional.md)。

## 安全

- 禁止提交 API Key / edu 密钥  
- `.env` 仅服务器本地；仓库只收 `.env.example`  

## 状态

`BINDING · 主线 = Dify Web + DeepSeek + 现网` · 正本见 CANON。  
**下一刀：** 现网 Docker 部署 Dify → 配 DeepSeek → 浏览器 G1 → 回写 Issue #1 与 `upstream/PIN.md`。
