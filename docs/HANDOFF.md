# HANDOFF · Aivia Workbench 总管交接

```
DOC: docs/HANDOFF.md
DATE: 2026-08-05
STATUS: BINDING · 新窗唯一入口（开场先读 docs/CANON.md）
FROM: 执行总管窗
TO: 后续执行/审查窗
UPDATED: 2026-08-05 · 阶段 A 功能出口收口；下一刀 = 入口硬化 + 阶段 B；OpenWork = 二期
```

---

## 0. 你是谁 · 怎么接

1. 新开对话，**先读** [`docs/CANON.md`](./CANON.md) + **本文全文** + [`ops/PHASE-A-CLOSEOUT.md`](../ops/PHASE-A-CLOSEOUT.md) + `ops/INFRA.md`  
2. 报约 **15 行状态**（见 §5 模板）再干活  
3. 真源只认：  
   - **主仓：** https://github.com/juanwan99/aivia-workbench  
   - **主底座上游：** https://github.com/langgenius/dify  
   - **旧仓 pico：** https://github.com/juanwan99/pico — 大功能冻结  
   - **基础设施：** §3.1 / `ops/INFRA.md`  
4. 禁止：密钥进仓、自 PASS、空成功当绿、Pico 大包、拆 WB 闭源、Dify/OpenWork 双主线  
5. 冲突 → **CANON + 本文最新 UPDATED**  

---

## 1. 北极星（一句话）

> **浏览器打开域名** → 登录 → 任务 → Agent/工作流真执行 → **可下载产物** → 停/重试 → **状态诚实**。  
> 模型默认 **DeepSeek**。业务 **edu-core** 后置桥。  
> 对标 WorkBuddy **响应逻辑**（clean-room）。

**禁止：** 「终态成功但无文件」。

---

## 2. 主线决策（BINDING）

| # | 决策 |
|---|------|
| D1 | 主仓 aivia-workbench，非 Pico 大包 |
| **D2** | **基线 = Dify Web**；不乱 fork 核 |
| D3 | 模型 DeepSeek API |
| D4 | 改：配置/应用/工作流/交付规则/品牌/后置 edu |
| D5 | 不改：无必要重写 Agent 框架；不像素抄 WB |
| D6 | AI 不直写 edu 业务库 |
| D9 | 沿用现网服务器/域名 |
| D10 | OpenWork = **二期**，不占主入口 |

---

## 3.1 服务器 · 域名（BINDING）

| 资源 | 状态 |
|------|------|
| 机器 | 沿用现网（IP/SSH **不进 Git**） |
| 域名 | `aivia.asia` 体系 |
| **主入口** | **`https://workbench.aivia.asia`** → Dify |
| pico 子域 | 过渡保留，大功能冻结 |
| 证书 | **A 阶段临时自签** → 正式证书见 CLOSEOUT R-A1 |

```text
同一机器（示意）
├── pico.aivia.asia        → 旧 Pico（冻结）
└── workbench.aivia.asia   → Dify Web 主台
```

---

## 4. 仓与文档地图

| 路径 | 用途 |
|------|------|
| [docs/CANON.md](./CANON.md) | 正本 |
| [ops/PHASE-A-CLOSEOUT.md](../ops/PHASE-A-CLOSEOUT.md) | **A 收口与残留风险** |
| [ops/PHASE-A-PACK.md](../ops/PHASE-A-PACK.md) | A 执行包 |
| [docs/PROJECT-PLAN.md](./PROJECT-PLAN.md) | 阶段 A–D |
| [upstream/PIN.md](../upstream/PIN.md) | 版本钉 + A 验收摘要 |
| [ops/INFRA.md](../ops/INFRA.md) | 基建 |
| [docs/DELIVERY-RULES.md](./DELIVERY-RULES.md) | B 纪律 |

**Issue：** https://github.com/juanwan99/aivia-workbench/issues/1  

---

## 5. 新窗开场 · 状态报告模板

```text
【状态】Aivia Workbench 交接后首报
主仓: juanwan99/aivia-workbench @ <sha>
正本: CANON = Dify Web + DeepSeek + 现网
主底座: Dify pin=1.16.1 · DeepSeek deepseek-chat
入口: https://workbench.aivia.asia
阶段: A 功能出口已收 · 入口硬化 OPEN（见 PHASE-A-CLOSEOUT）
下一刀: 清 R-A1/R-A2（证书+公网可达）→ 阶段 B 纪律/课件 10 次空成功=0
已拍板: Web+Dify+DeepSeek；OpenWork=二期；空成功禁止；edu 后置
阻塞: <证书/WAF/…>
不做什么: Pico 大包、OpenWork 当主线、密钥进仓、无证据自 PASS
请业主: <仅授权时>
```

---

## 6. 当前进度

| 项 | 状态 |
|----|------|
| 云端 Web 优先 / 主底座 Dify | **已定** |
| 正本清源 CANON | **已落盘** |
| 现网安装 Dify 1.16.1 | **已做**（PIN） |
| DeepSeek | **已做** |
| 默认课件入口 | **已做** |
| G0 / G0b / G1 / G1+ | **功能 PASS**（PIN） |
| 正式 HTTPS / 公网无 403 | **未完成**（R-A1/R-A2） |
| G4 反空成功 | **未测**（R-A3） |
| 阶段 B 十次空成功清零 | **未做** |
| edu 桥 | **未做**（须授权） |
| OpenWork | **二期** |

**下一刀：**  
1) 运维消化 `ops/PHASE-A-CLOSEOUT.md` 中 **R-A1、R-A2**  
2) 然后阶段 **B**：交付纪律 + 课件稳定 + 10 次空成功=0  

---

## 7. 阶段速查

| 阶段 | 目标 | 出口 |
|------|------|------|
| **A** | 现网 Dify + DS + 出文件 | G0–G1+ 功能绿 · 入口硬化跟进 |
| **B** | 交付纪律 + 课件应用 | 空成功=0 |
| **C** | edu JWT 桥 | 授权后 |
| **D** | 试点 | 小范围教师 |

---

## 8–10. 纪律与禁止

不自 PASS；密钥不进 Issue；工程绿 ≠ 产品绿。  
禁止：Pico 大包；OpenWork 写回主线；无 G 证据宣称完成；未备份拆 pico 域名。

---

## 11. 行动令（当前）

```text
1) 读 CANON + HANDOFF + PHASE-A-CLOSEOUT + PIN
2) 按 §5 打状态（勿再说「下一刀=装 Dify」）
3) 优先：正式证书 + 公网可达复验
4) 通过后开阶段 B（DELIVERY-RULES + 10 次要课件）
5) 结果回写 Issue #1
```

---

**交接完成条件：** 新窗承认：A **功能**已 PIN 收口；**入口硬化**与 **B** 为当前工作，而非重新安装 OpenWork/Dify 大叙事。
