# HANDOFF · Aivia Workbench 总管交接

```
DOC: docs/HANDOFF.md
DATE: 2026-08-05
STATUS: BINDING · 新窗唯一入口
FROM: 前总管窗（Pico 收尾 → OpenWork 选型 → 建仓）
TO: 新开 Grok/执行总管窗
UPDATED: 补 §3.1 服务器/域名/IP（此前口头有、文档曾缺，已补全）
```

---

## 0. 你是谁 · 怎么接

1. 新开对话，**先读本文全文** + `docs/PROJECT-PLAN.md` + `ops/INFRA.md`  
2. 报约 **15 行状态**（见 §5 模板）再干活  
3. 真源只认：  
   - **主仓：** https://github.com/juanwan99/aivia-workbench  
   - **上游成品：** https://github.com/different-ai/openwork （OpenCode）  
   - **旧仓 pico：** https://github.com/juanwan99/pico — **大功能冻结**，仅安全/停机级  
   - **基础设施：** 见 §3.1 / `ops/INFRA.md`（**沿用旧服务器与域名**）  
4. 禁止：密钥进仓、自 PASS、空成功当绿、再开 Pico 大叙事包、拆 WorkBuddy 闭源  

---

## 1. 北极星（一句话）

> 任务 → Agent **真工具循环** → **工作区可下载产物** → 停/重试 → **状态诚实**。  
> 模型默认 **DeepSeek**。业务真源 **edu-core**（后置桥）。  
> 体验对标 WorkBuddy **响应逻辑**（clean-room），不抄皮、不拆包盗码。

**禁止：** 「终态成功但无文件」。

---

## 2. 为什么离开 Pico 主线

| 事实 | 结论 |
|------|------|
| 长周期 PASS/门禁多，办公「出文档」不稳 | 用户极度不满 |
| 截图：成功 98s、暂无产物 | 验收尺子错（API 金路径 ≠ 真人多轮） |
| 业主要 DeepSeek + 强 Agent + 能跑 | 自研半吊子环不值得再堆 |
| WorkBuddy 本机 clean-room | 学的是：**壳 + 独立 Agent serve + 工作区写盘 + 账本 + 产物** |
| 成品仓调研 | 定 **OpenWork**（已拼好，powered by OpenCode） |

---

## 3. 已拍板决策（勿重新辩论除非业主改口）

| # | 决策 |
|---|------|
| D1 | 新主线仓 **aivia-workbench**，不是继续 Pico 大包 |
| D2 | 基线成品 **OpenWork**；Agent 核 **OpenCode** — **不重写核** |
| D3 | 模型 **DeepSeek** BYOK |
| D4 | 改：配置 / Skills / 交付规则 / 品牌 / 后置 edu 桥 |
| D5 | 不改：OpenCode 主循环、任务-工作区主模型、为像素抄 WB 大改 UI |
| D6 | edu-core = 业务真源；AI 只读/提案，不直写业务库 |
| D7 | WorkBuddy 只作响应逻辑对标；OpenWork **产品完整度弱于 WB**，开放与可改强于 WB |
| D8 | 成品仓 > 继续空想七层零件；但学校 SaaS 仍可能要薄桥，不幻想开箱 edu |
| **D9** | **基础设施：继续用现有服务器 / 公网 IP / 域名体系**，不强制换机换域名（见 §3.1） |

### 曾调研但未作主底座的（避免回潮）

- 零件：Dify / Open WebUI / LibreChat / n8n / Reasonix…（可作参考，**当前主线不是它们**）  
- 其它成品：AionUi、Eigent = **OpenWork 失败时的备选**，不是现在双主线  

---

## 3.1 服务器 · 域名 · IP（BINDING）

> 业主 2026-08-05 确认口径：**可以继续用之前的服务器和域名 IP。**  
> 详细运维说明：[`ops/INFRA.md`](../ops/INFRA.md)

| 资源 | 决策 |
|------|------|
| **机器 / 公网 IP** | **沿用**现有 Pico 所在服务器（或同集群），**不要求**新购机器才能开工 |
| **域名** | **沿用** `aivia.asia` 体系（含历史 `pico.aivia.asia` 等） |
| **OpenWork 跑哪** | **阶段 A/B：教师/开发者本机桌面客户端**，不是「把 OpenWork 当成旧 Pico 同构 Web 整站替换」 |
| **服务器上仍要干什么** | 过渡保留 Pico；下载/文档/健康检查；日后 **edu 桥 / 配置下发 / 可选 Web 门户** |
| **域名怎么分** | 建议：`pico.aivia.asia` 过渡期保留旧站；新入口可用子域如 `workbench.aivia.asia` 或 `desk.aivia.asia`（下载+说明+日后网关）。**反代分流**，避免两服务抢死同一用途 |
| **证书 HTTPS** | 旧域名续期；新子域加证书即可 |
| **密钥** | DeepSeek 等可放服务器保管或客户端 BYOK；**禁止进 Git** |
| **禁止** | 未评估就清空服务器、或把客户端硬编码死绑旧 Pico Agent API 当核 |

```text
同一 IP/机器（示意）
├── pico.aivia.asia     → 旧 Pico（冻结大功能，可缩容）
├── workbench.aivia.asia → 新：静态说明/下载/日后桥（阶段 C）
└── 客户端 OpenWork      → 用户本机 + DeepSeek
```

**阶段 A 不依赖** 先改 DNS 才能装 OpenWork；本机 G1 优先。

---

## 4. 仓与文档地图

| 路径 | 用途 |
|------|------|
| [README.md](../README.md) | 总览 |
| [docs/PROJECT-PLAN.md](./PROJECT-PLAN.md) | 阶段 A–D、里程碑 |
| [docs/ARCHITECTURE.md](./ARCHITECTURE.md) | 分层 |
| [docs/CHANGE-POLICY.md](./CHANGE-POLICY.md) | 改/不改 |
| [docs/GOLD-PATHS.md](./GOLD-PATHS.md) | G0–G4 |
| [docs/RESPONSE-LOGIC.md](./RESPONSE-LOGIC.md) | R1–R8 |
| [ops/INSTALL.md](../ops/INSTALL.md) | 安装 |
| [ops/INFRA.md](../ops/INFRA.md) | **服务器/域名/IP** |
| [ops/deepseek.env.example](../ops/deepseek.env.example) | DS 样例 |
| [upstream/PIN.md](../upstream/PIN.md) | **待填** 版本钉 |
| [docs/HANDOFF.md](./HANDOFF.md) | 本文 |

**Issue：** https://github.com/juanwan99/aivia-workbench/issues/1 （M0/M1）  
**Pico 交接旧真源：** pico#273（历史）；新工作以 aivia-workbench 为准  

---

## 5. 新窗开场 · 状态报告模板（约 15 行）

```text
【状态】Aivia Workbench 交接后首报
主仓: juanwan99/aivia-workbench @ <sha>
上游: OpenWork pin=<未填则写未装>
基建: 沿用现网 IP/域名（见 HANDOFF §3.1）；阶段A=本机客户端
阶段: A 跑通 | 下一刀: 安装+DS+G1
已拍板: OpenWork+DeepSeek；不改 Agent 核；空成功禁止；不换机也可开工
阻塞: <无 / 列出>
不做什么: Pico 大包、Dify 改主线、拆 WB、清空旧服无回滚
请业主: <仅当需要授权时>
```

---

## 6. 当前进度（交接时刻）

| 项 | 状态 |
|----|------|
| 选型 OpenWork | **已定** |
| 建仓 + 规划文档 | **已完成** |
| 服务器/域名策略 | **已定：沿用**（§3.1；曾口头后补进文档） |
| 本机安装 OpenWork | **未做**（业主/执行窗） |
| DeepSeek 配置 | **未做** |
| G1 金路径 | **未做** |
| Skills 课件包 | **未做**（阶段 B） |
| edu 桥 | **未做**（阶段 C，须授权） |
| pico 线上 | 旧系统仍在；**新功能不进 pico** |

**下一刀（唯一）：**  
`ops/INSTALL.md` → DeepSeek → `GOLD-PATHS` G0/G0b/G1 → 回写 Issue #1 + `upstream/PIN.md`。  
**不阻塞于** 先改域名；DNS 子域可与 G1 并行。

---

## 7. 阶段速查

| 阶段 | 目标 | 出口 |
|------|------|------|
| **A** | 装上 + DS + 出文件 | G1 绿 |
| **B** | 交付纪律 + 课件 Skill | 空成功=0 |
| **C** | edu JWT 桥（可挂旧服务器） | 身份入任务（授权后） |
| **D** | 试点 | 小范围教师 |

---

## 8. 任务卡纪律（若派执行窗）

业主曾纠正标准卡格式（勿发明其它格式）：

```text
════════════════════════════════════
标准任务卡 · <任务代号>
════════════════════════════════════
执行窗：…
上下文：CLEAR
角色：…
RISK: 红/黄/绿
FAST: 是/否
仓 / 载体回写 / BASE 或 TARGET
关联 Issue
【你是谁】…禁止项
【真源】…
【阶段 A】…
【阶段 B】…
【禁止 · OUT】…
【CLAIM】…
【回写】…
════════════════════════════════════
```

- 不自 PASS；eligible 由审查说  
- 密钥、联合键不进 Issue  
- 工程绿 ≠ 产品绿  

---

## 9. 业主偏好与雷区（硬）

| 要 | 不要 |
|----|------|
| 人话、进度诚实 | 假 PASS、空成功 |
| 响应逻辑对标 WB | 只学三栏布局 |
| 成品仓少自焊 | 再堆 Pico 门禁大包 |
| DeepSeek | 默认绑 Kimi/Claude 当底座 |
| **沿用现网 IP/域名** | 无必要换机换域、清空旧服无过渡 |
| 交接触达「改什么不改」 | 一上来重写 OpenCode |

**情绪背景：** 对 Pico「连简单任务都做不好」极不满；长任务/复杂任务要对标主流 Agent 台。新线用 OpenWork 是 **换底座自救**，不是再画饼。

---

## 10. 首周禁止清单

1. 在 pico 开 P-COMPLEX / 大残留包  
2. 并行主推 Dify/AionUi/Eigent（除非 OpenWork G1 失败并业主改口）  
3. 无 G1 就做 edu 全量  
4. 提交 API Key  
5. 宣称「已对标 WorkBuddy 完成」无金路径证据  
6. **未备份/未分流就下线 pico 域名或清空服务器**  

---

## 11. 给新窗的第一封行动令

```text
1) 读 docs/HANDOFF.md + PROJECT-PLAN.md + CHANGE-POLICY.md + ops/INFRA.md
2) 按 §5 打状态报告（含基建：沿用 IP/域名）
3) 派或自执行：安装 OpenWork + DeepSeek + G1（本机，不依赖先改 DNS）
4) 结果写入 aivia-workbench#1 与 upstream/PIN.md
5) G1 绿后才开阶段 B；子域/下载页可并行，非 P0 阻塞
```

---

## 12. 联系真源索引（历史）

| 主题 | 位置 |
|------|------|
| Pico 旧交接 | pico#273 |
| 开源零件调研 | pico#306 |
| 架构草案（七层） | pico#307 |
| 一体/成品调研 | pico#308 |
| WorkBuddy 本机报告 | 业主本地 md（clean-room，勿进仓盗码） |
| 新仓规划 | **本仓 docs/** |
| **服务器/域名** | **本仓 §3.1 + ops/INFRA.md** |

---

**交接完成条件：** 新窗已用 §5 打出首报（含基建口径），且承认下一刀 = OpenWork 安装与 G1。
