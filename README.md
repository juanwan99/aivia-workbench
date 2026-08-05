# Aivia Workbench

学校 / 办公向 **AI Agent 工作台**（任务 → 过程 → 产物 → 停/重试 → 状态诚实）。

| 项 | 决策 |
|----|------|
| **基线成品** | [OpenWork](https://github.com/different-ai/openwork)（powered by OpenCode） |
| **模型** | **DeepSeek**（默认） |
| **业务真源** | edu-core（后置对接；AI 不直写业务库） |
| **体验对标** | WorkBuddy **响应逻辑**（clean-room，不抄闭源） |
| **旧仓** | `juanwan99/pico` 冻结大功能；本仓为新主线 |

## 一句话目标

> 老师/用户下任务 → Agent 真工具循环 → **工作区有可下载产物** → 失败诚实可再试。  
> **禁止「终态成功但无文件」。**

## 仓库结构（规划）

```text
docs/                 规划与纪律（本阶段主内容）
upstream/             OpenWork 上游说明与 pin 版本（不vend整个巨仓时可只记 pin）
skills/               我们自建的课件/文档 Skills
bridge/               edu JWT / 身份桥（后置）
ops/                  安装、DeepSeek 配置样例（无密钥）
```

## 文档入口

| 文档 | 内容 |
|------|------|
| [docs/PROJECT-PLAN.md](./docs/PROJECT-PLAN.md) | **总规划**（阶段、里程碑、验收） |
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | 架构与分层 |
| [docs/CHANGE-POLICY.md](./docs/CHANGE-POLICY.md) | **改什么 / 不改什么** |
| [docs/GOLD-PATHS.md](./docs/GOLD-PATHS.md) | 金路径验收 |
| [docs/RESPONSE-LOGIC.md](./docs/RESPONSE-LOGIC.md) | WorkBuddy 向响应逻辑清单 |
| [docs/DELIVERY-RULES.md](./docs/DELIVERY-RULES.md) | 交付硬规则（阶段 B） |
| [ops/INSTALL.md](./ops/INSTALL.md) | **本机安装 + DeepSeek + 金路径** |
| [ops/G-PATH-RUNBOOK.md](./ops/G-PATH-RUNBOOK.md) | G0–G4 勾选清单 |

## 与 OpenWork 关系

- **上游：** https://github.com/different-ai/openwork  
- **策略：** 配置 + Skills + 薄桥优先；不重写 OpenCode 核  
- **许可：** 遵循上游 LICENSE；自研文件见本仓声明  

## 安全

- 禁止提交 API Key / edu 密钥  
- `.env` 仅本地；仓库只收 `.env.example`  

## 状态

`A+B 任务包已落盘`（安装文档 / DeepSeek 样例 / 金路径清单 / 交付规则 / 课件·教案 Skills 骨架）。  
**下一刀（本机）：** 按 [ops/INSTALL.md](./ops/INSTALL.md) 安装 OpenWork + DeepSeek + **G1 真文件** → 回写 Issue #1 与 `upstream/PIN.md`。  
G1 未绿前不宣称阶段 A 完成、不启用阶段 B 实测。
