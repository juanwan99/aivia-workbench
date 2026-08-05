# HANDOFF · Aivia Workbench 总管交接

```
DOC: docs/HANDOFF.md
DATE: 2026-08-05
STATUS: BINDING · 新窗唯一入口
FROM: 前总管窗（Pico 收尾 → 曾选 OpenWork → 建仓）
TO: 新开执行总管窗
UPDATED: 2026-08-05 · 业主新口径覆盖：主线 = Dify Web + DeepSeek + 现网；OpenWork = 二期可选
```

---

## 0. 你是谁 · 怎么接

1. 新开对话，**先读本文全文** + `docs/PROJECT-PLAN.md` + `ops/INFRA.md` + `docs/SELECTION-WEB-v2.md`  
2. 报约 **15 行状态**（见 §5 模板）再干活  
3. 真源只认：  
   - **主仓：** https://github.com/juanwan99/aivia-workbench  
   - **主底座上游：** https://github.com/langgenius/dify （Web 工作台）  
   - **旧仓 pico：** https://github.com/juanwan99/pico — **大功能冻结**，仅安全/停机级  
   - **基础设施：** 见 §3.1 / `ops/INFRA.md`（**沿用现有服务器与域名**）  
4. 禁止：密钥进仓、自 PASS、空成功当绿、再开 Pico 大叙事包、拆 WorkBuddy 闭源、**Dify 与 OpenWork 双主线并列**  

---

## 1. 北极星（一句话）

> **浏览器打开域名** → 登录 → 任务 → Agent/工作流 **真执行** → **可下载产物** → 停/重试 → **状态诚实**。  
> 模型默认 **DeepSeek**。业务真源 **edu-core**（后置桥）。  
> 体验对标 WorkBuddy **响应逻辑**（clean-room），不抄皮、不拆包盗码。  
> 中心化知识库/模板由平台治理，不指望老师本机建库。

**禁止：** 「终态成功但无文件」。

---

## 2. 为什么离开 Pico · 以及为何不再以 OpenWork 为主线

| 事实 | 结论 |
|------|------|
| Pico 长周期「出文档」不稳、空成功 | 换底座自救 |
| 产品原定义 = **浏览器/公网工作台** | 与桌面-only 主线不对齐 |
| 业主要云端优先、挂现网服务器+域名 | 需要 Web 自托管平台 |
| 选型调查 v2 | **Dify** 更适合作云端主台 |
| OpenWork | **二期**本地文件增强，不是默认主入口 |

---

## 3. 已拍板决策（勿重新辩论除非业主再改口）

| # | 决策 |
|---|------|
| D1 | 新主线仓 **aivia-workbench**，不是继续 Pico 大包 |
| **D2** | **基线 = Dify（Web）**；Agent/工作流以 Dify 应用与画布为主 — **不乱 fork Dify 核** |
| D3 | 模型 **DeepSeek** API |
| D4 | 改：DS 配置、应用/工作流、交付规则、品牌、后置 edu 桥、知识库/模板 |
| D5 | 不改：无必要重写 Agent 框架；不为像素抄 WB 大改 UI；不拆闭源 |
| D6 | edu-core = 业务真源；AI 只读/提案，**不直写**业务库 |
| D7 | WorkBuddy 只作响应逻辑对标 |
| D8 | OnlyOffice 等云端 Office 精修 = **后置可选**；先模板生成 + 下载 |
| **D9** | **基础设施：继续用现有服务器 / 公网 IP / 域名**，不强制换机 |
| **D10** | **OpenWork / 桌面客户端 = 二期可选**，不占主 README/主入口；禁止与 Dify 双主线 |

### 曾调研但当前不作主底座的

- Open WebUI / LibreChat / FastGPT / n8n 等：可参考或对照 Spike，**主线不是它们**  
- OpenWork / AionUi / Eigent：**二期或备选本地**，不是现在默认入口  

---

## 3.1 服务器 · 域名 · IP（BINDING）

> 业主确认：**继续用之前的服务器和域名 IP。** 详见 [`ops/INFRA.md`](../ops/INFRA.md)

| 资源 | 决策 |
|------|------|
| **机器 / 公网 IP** | **沿用**现有服务器（或同集群） |
| **域名** | **沿用** `aivia.asia` 体系 |
| **Dify 跑哪** | **现网 Docker**；主入口建议 `workbench.aivia.asia`（或业主指定子域）→ 反代到 Dify |
| **pico.aivia.asia** | 过渡保留旧站；大功能冻结 |
| **OpenWork** | 不占主入口；二期本机可选 |
| **证书 HTTPS** | 旧域续期；新子域加证书 |
| **密钥** | 仅服务器 env / 密钥库；**禁止进 Git** |

```text
同一 IP/机器（示意）
├── pico.aivia.asia        → 旧 Pico（冻结，可缩容）
├── workbench.aivia.asia   → Dify Web 主台（阶段 A 目标入口）
└── （二期）本机 OpenWork   → 可选本地文件增强
```

---

## 4. 仓与文档地图

| 路径 | 用途 |
|------|------|
| [README.md](../README.md) | 总览（Web + Dify + DS） |
| [docs/PROJECT-PLAN.md](./PROJECT-PLAN.md) | 阶段 A–D |
| [docs/SELECTION-WEB-v2.md](./SELECTION-WEB-v2.md) | 选型结论（已确认云端优先） |
| [docs/ARCHITECTURE.md](./ARCHITECTURE.md) | 分层 |
| [docs/CHANGE-POLICY.md](./CHANGE-POLICY.md) | 改/不改 |
| [docs/GOLD-PATHS.md](./GOLD-PATHS.md) | 浏览器金路径 |
| [docs/DELIVERY-RULES.md](./DELIVERY-RULES.md) | 交付纪律 |
| [ops/INSTALL.md](../ops/INSTALL.md) | **Dify Docker + DS** |
| [ops/INFRA.md](../ops/INFRA.md) | 服务器/域名 |
| [ops/INSTALL-OPENWORK-optional.md](../ops/INSTALL-OPENWORK-optional.md) | 二期桌面（非主线） |
| [upstream/PIN.md](../upstream/PIN.md) | 版本钉（Dify 为主） |

**Issue：** https://github.com/juanwan99/aivia-workbench/issues/1  

---

## 5. 新窗开场 · 状态报告模板（约 15 行）

```text
【状态】Aivia Workbench 交接后首报
主仓: juanwan99/aivia-workbench @ <sha>
主底座: Dify pin=<未装则写未装> · 模型 DeepSeek
基建: 沿用现网 IP/域名（HANDOFF §3.1）；入口 workbench 子域 → Dify
阶段: A 跑通 | 下一刀: 现网 Docker 装 Dify + DS + 浏览器 G1
已拍板: Web+Dify+DeepSeek；OpenWork=二期；空成功禁止；edu 后置
阻塞: <无 / 列出>
不做什么: Pico 大包、OpenWork 当主线、双主线、拆 WB、密钥进仓
请业主: <仅当需要授权时>
```

---

## 6. 当前进度

| 项 | 状态 |
|----|------|
| 云端 Web 优先口径 | **已确认** |
| 主底座 Dify | **已定**（选型 v2 + 业主拍板） |
| 建仓 + 规划文档 | **已按新口径改写** |
| 服务器/域名策略 | **已定：沿用** |
| 现网安装 Dify | **未做** |
| DeepSeek 配置 | **未做** |
| 浏览器 G1 | **未做** |
| 课件应用/工作流 | **未做**（阶段 B） |
| edu 桥 | **未做**（阶段 C，须授权） |
| OpenWork | **二期**，非当前下一刀 |

**下一刀（唯一）：**  
`ops/INSTALL.md` → 现网 Docker 部署 Dify → DeepSeek → `GOLD-PATHS` G0/G0b/G1（浏览器）→ 回写 Issue #1 + `upstream/PIN.md`。

---

## 7. 阶段速查

| 阶段 | 目标 | 出口 |
|------|------|------|
| **A** | 现网 Dify + DS + 浏览器出文件 | G1 绿 |
| **B** | 交付纪律 + 课件应用/工作流 | 空成功=0 |
| **C** | edu JWT 桥 | 身份入任务（授权后） |
| **D** | 试点；本地客户端可选 | 小范围教师 |

---

## 8. 任务卡纪律

（格式不变，略；不自 PASS；密钥不进 Issue；工程绿 ≠ 产品绿。）

---

## 9. 业主偏好与雷区（硬）

| 要 | 不要 |
|----|------|
| 人话、进度诚实 | 假 PASS、空成功 |
| **浏览器公网工作台** | 把桌面 OpenWork 写成主入口 |
| DeepSeek + 真 Agent/工作流 | 纯闲聊壳 |
| 中心化知识库/模板 | 只靠老师本机建库 |
| **沿用现网 IP/域名** | 无必要换机、清空旧服无过渡 |
| 成品少自焊 | 再堆 Pico 门禁大包 / 乱 fork Dify 核 |

---

## 10. 首周禁止清单

1. 在 pico 开大功能包  
2. **把 OpenWork 写回主线或与 Dify 双主入口**  
3. 无 G1 就做 edu 全量  
4. 提交 API Key  
5. 无金路径证据宣称交付完成  
6. 未备份就下线 pico 域名或清空服务器  

---

## 11. 给新窗的第一封行动令

```text
1) 读 HANDOFF + PROJECT-PLAN + CHANGE-POLICY + INFRA + SELECTION-WEB-v2
2) 按 §5 打状态报告（主底座=Dify Web）
3) 现网：Docker 装 Dify + DeepSeek + 浏览器 G1
4) 结果写入 Issue #1 与 upstream/PIN.md
5) G1 绿后才开阶段 B；OpenWork 仅二期
```

---

## 12. 联系真源索引（历史）

| 主题 | 位置 |
|------|------|
| Pico 旧交接 | pico#273 |
| 选型零件/一体调研 | pico#306–308 |
| **Web 选型 v2** | **docs/SELECTION-WEB-v2.md** |
| 服务器/域名 | §3.1 + ops/INFRA.md |

---

**交接完成条件：** 新窗已用 §5 打出首报，且承认下一刀 = **现网 Dify + DeepSeek + 浏览器 G1**（不是装 OpenWork 桌面）。
