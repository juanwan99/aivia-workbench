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
| 阶段 B 10 次空成功 | **0** |
| B-HARDEN 应用侧（H1/H3/H7） | **绿** |
| DEBT-CLEAR E2–E8 | **应用/回归可报**（E8 空成功 0） |
| 正式 HTTPS 无警告（E1） | **BLOCKED**（需 DNS-01） |
| **CLAIM-B 教师正式可用** | **否**（E1 未满） |
| **下一刀** | DNS-01 正式证书 |

## 文档

| 文档 | 内容 |
|------|------|
| [CANON](./docs/CANON.md) | 正本 |
| [HANDOFF](./docs/HANDOFF.md) | 交接 |
| [PHASE-DEBT-CLEAR-PACK](./ops/PHASE-DEBT-CLEAR-PACK.md) | 债务清零执行包 |
| [DEBT-CLEAR-RUNBOOK](./ops/DEBT-CLEAR-RUNBOOK.md) | 勾选结果 |
| [PIN](./upstream/PIN.md) | 版本钉 |

## 二期

OpenWork 桌面可选，非主入口。

## 安全

禁止 API Key / 公网 IP / SSH 进仓。
