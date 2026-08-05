# Aivia Workbench

学校 / 办公向 **浏览器公网 AI Agent 工作台**（任务 → 过程 → **可下载产物** → 状态诚实）。

| 项 | 决策 |
|----|------|
| 形态 | Web / 公网 |
| 底座 | [Dify](https://github.com/langgenius/dify) 自托管 **1.16.1** |
| 模型 | DeepSeek |
| **默认入口（唯一主推）** | https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl |
| 正本 | [docs/CANON.md](./docs/CANON.md) |

## 状态

| 项 | 状态 |
|----|------|
| 阶段 A 功能 | **绿** |
| 阶段 B 10 次空成功 | **0**（纪律有条件绿） |
| B-HARDEN 应用侧（H1/H3/H7） | **绿** |
| 正式 HTTPS 无警告 | **未满**（自签；H2） |
| **下一刀** | 正式证书（DNS-01/云厂商）或授权后 edu 桥 |

## 文档

| 文档 | 内容 |
|------|------|
| [CANON](./docs/CANON.md) | 正本 |
| [HANDOFF](./docs/HANDOFF.md) | 交接 |
| [PHASE-B-CLOSEOUT](./ops/PHASE-B-CLOSEOUT.md) | B/Harden 收口 |
| [B-HARDEN-RUNBOOK](./ops/B-HARDEN-RUNBOOK.md) | 硬化勾选结果 |
| [PIN](./upstream/PIN.md) | 版本钉 |

## 二期

OpenWork 桌面可选，非主入口。

## 安全

禁止 API Key / 公网 IP / SSH 进仓。
