# 阶段 B 收口纪要 · 有条件关闭

```
DATE: 2026-08-05
STATUS: 纪律电池有条件绿 · 硬化 OPEN
证据: upstream/PIN.md · ops/B-PATH-RUNBOOK.md · Issue #1 B 回写
审查: 有条件 M3 · 综合约 6.5–7/10 · 禁止对外「教师正式可用」
```

## 1. 已确认完成（纪律 / 功能）

| 项 | 证据 |
|----|------|
| 10 次电池空成功 = 0 | RUNBOOK T1–T10 + PIN + Issue |
| B0 G4 反空成功 | RUNBOOK / Issue（拒假大文件） |
| 默认应用「Aivia 课件」Chatflow | 公开 `/chat/lOMVPbz7rZmbJSJl` |
| 系统提示强制出件 | B1 |
| HTML 多主题 + 同会话改稿 | T1–T3/T5/T6/T8 |
| 教案可下载（**MD**） | T4 |
| 平台结构模板/知识库最低集 | B5 economy |
| T9 首轮 FAIL 后修复 | 诚实履历，非一路假绿 |

**含义：** 「要文件不空成功」在内测电池上成立。  
**不等于：** 已对齐 WorkBuddy 交付形态；不等于公网无警告可试点。

## 2. 审查纠偏（禁止继续虚报）

| 原 CLAIM | 纠偏 |
|----------|------|
| B0–B5 **全 PASS** | **B3 改为部分完成**（见下） |
| M3 无条件绿 | **M3 有条件**（纪律电池） |
| 可对外使用 | **否**，直至 R-A1/R-A2 + 本 Harden 关键项 |

### B3 纠偏

已做：`max_tokens` / `temperature` 起点 + 失败人话。  
**未做：** 工作空间/用户 **日调用配额**、真正超时熔断、触发限额后的产品级提示。  
→ 记 **B3 = PARTIAL**，硬化包 **H3** 必做。

## 3. 残留风险登记（必须消化）

| ID | 风险 | 严重度 | 硬化包 |
|----|------|--------|--------|
| **R-B1** | 交付=代码块另存，非平台文件附件 | 高 | H1 |
| **R-B2** | HTTPS 自签警告 | 高 | H2（=R-A1） |
| **R-B3** | 公网 403 / 可达不稳定 | 高 | H2（=R-A2） |
| **R-B4** | 真配额未钉 | 中高 | H3 |
| **R-B5** | 教案仅 MD，非 DOCX | 中 | H4 |
| **R-B6** | 双入口（旧 Agent + 新 Chatflow）易混 | 中 | H5 |
| **R-B7** | 产物仅服务器路径，仓内无抽检样例 | 中 | H6 |
| **R-B8** | HANDOFF/PLAN/README 仍写「去做 B」 | 中 | H0（本文同步） |
| **R-B9** | 无 embedding，知识库 weak | 低 | 后置可选 |
| **R-B10** | Issue 历史含 IP 明文 | 低 | 勿再贴；旧评不删履历 |

## 4. 默认入口（现行）

| 角色 | URL / 名 |
|------|----------|
| **默认（B 后）** | `https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl` · **Aivia 课件** Chatflow |
| 备用 | 旧 Agent site `dV3HeqgfVt4Xmm7f` · 仅排障，不主推教师 |

## 5. 下一刀

见 [`ops/PHASE-B-HARDEN-PACK.md`](./PHASE-B-HARDEN-PACK.md) · 任务卡 **PHASE-B-HARDEN**。  
**禁止**未硬化就开阶段 C 全量或对外试点话术。
