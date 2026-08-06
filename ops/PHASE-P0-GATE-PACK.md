# 大包 · P0 稳定 + 金路径体感 + 双门（CLAIM-B / full real）

```
STATUS: BINDING · 计划写实 · 待授权执行
DATE: 2026-08-06
CODE: PHASE-P0-GATE
前提: A/B/C-hybrid/D-LITE/E1(仓内PASS) 已收 · CLAIM-B 未勾 · full real 未做
形态: 浏览器 Dify Web + DeepSeek · 非 OpenCode Harness
对标: ChatGPT / Gemini / 一线教育 WebAgent 的「打开即用、过程可见、失败诚实、产物可下」
```

> **本包是「完善优化」主计划，不是重开 A/B/C。**  
> **禁止** 空成功、口头完毕、假 CLAIM-B、假 full real、公网裸 bridge、密钥进仓。  
> **交付 = 真文件进仓 + RUNBOOK 勾满 + PIN/CANON 一句 + Issue 回写。**

---

## 0. 产品目标（对标一线，不是花架子）

用户心智（对标主流 AI 站 + 专业课件台）：

| 一线体验 | 我们本包必须做到 |
|----------|------------------|
| 打开链接就进工作区 | HTTPS 稳、无证书惊吓、首屏 ≤ 数秒有壳 |
| 说清意图就干活 | 推荐问题一点即发；话术可抄 |
| 过程可感 | 生成中有反馈；非无限白屏 |
| 要文件就有文件 | DOWNLOAD_READY / 可点下载；禁止空成功 |
| 不要文件就不装样 | 大纲/闲聊无假下载 |
| 失败人话 | 超时/限流/模型失败有说明 |
| 组织边界（进阶） | full real：本校只读、跨校 403 |

**明确不做（本包范围外）：**  
Codex/OpenCode Harness、OpenWork 主线、全校推广营销、Agent 写成绩库、OnlyOffice 精修。

---

## 1. 总结构（三波 · 可串行，2a/2b 业主二选一或先后）

```text
波 0  P0-STAB     稳定可达 + 续期 + 真源去滞后     ← 门：不过不进体感刷数
波 1  P0-GOLD     金路径体感 5 刀 + 证据进仓       ← 门：空成功=0 才谈 CLAIM-B
波 2a CLAIM-B     教师正式可用产品验收             ← 独立 CLAIM
波 2b FULL-REAL   edu live 只读 → C-REAL full      ← 独立 CLAIM · 可与 2a 并行研发
```

**建议默认顺序：** 0 → 1 → **先 2a（CLAIM-B）**；2b 在有 edu API 时插队或并行。  
**禁止：** 跳过 0/1 直接勾 CLAIM-B。

---

## 2. 波 0 · P0-STAB（稳定）

**目标：** 老师用域名打开不再「半天转圈 / 握手 RST」；证书可续；文档不说谎。

### 0.1 外网 HTTPS 压实

| 动作 | 验收 |
|------|------|
| 公网 `curl -vI https://workbench.aivia.asia/` | **TLS 完成** + HTTP 2xx/3xx（非 reset） |
| 本机 + 手机 4G 各开默认 Chat | 首屏可见「Aivia 课件」壳 |
| 若仍 SNI RST | 修 nginx workbench server SSL **或** WAF/Beaver 规则；记 `ops/evidence/p0-stab/tls-note.md` |
| HTTP 80 | 允许跳转 HTTPS；禁止长期 403 挡主路径（WAF 误杀要关） |

### 0.2 证书续期

| 动作 | 验收 |
|------|------|
| 优先路径 B：`acme.sh --dns dns_ali`（AK 仅服务器 secrets） | 文档写清续期命令；**不进 Git** |
| 若暂无 AK | 日历提醒 + 手工 TXT 步骤保留在 E1-RUNBOOK |
| 到期日 | PIN 写 ~2026-11-03 与续期策略 |

### 0.3 服务保活

| 动作 | 验收 |
|------|------|
| Dify / nginx / bridge 容器或 systemd | 重启策略仍在；`health` 200 |
| bridge 非公网裸奔 | ss/文档确认 |

### 0.4 真源扫尾

| 文件 | 动作 |
|------|------|
| README / CANON | 去掉「E1 BLOCKED / 自签仍在」旧句 |
| REMAINING-TASK-CARDS | 改为本包引用 |
| DEBT-LEDGER | 波 0 关闭项打勾 |

### 波 0 完成定义

```text
[ ] 公网域名 TLS 连续 3 次探测无 reset（或 ISSUE 记 WAF 残留+缓解）
[ ] 4G 或外网打开 Chat 有壳
[ ] 续期策略书面（自动或手工）
[ ] README/CANON 与 PIN 一致（E1 PASS）
[ ] RUNBOOK 波 0 勾满 + push + Issue 一句
```

---

## 3. 波 1 · P0-GOLD（金路径体感）

**目标：** 对标一线「说完就能用」——5 条金路径全真跑，证据进仓，**空成功 = 0**。

### 3.1 金路径表（对标）

| ID | 用户行为 | 对标 | 过线 |
|----|----------|------|------|
| **G1** | 「做×× HTML 课件，要能下载」 | ChatGPT 出可下文件感 | DOWNLOAD_READY + 真 HTML 可开有标题 |
| **G1+** | 同会话「改一版加 2 道题」 | 多轮改稿 | 仍有文件；非换会话才成功 |
| **G2** | 「写××教案可下载」 | 教案交付 | md/文件 + 下载；可声明非 Word |
| **G3** | 「只要大纲不要文件」 | 诚实 | **无**假 DOWNLOAD_READY |
| **G4** | 超时/故意难需求 或 限流提示 | 失败诚实 | 人话失败，不装成功 |

### 3.2 体感增强（有则改配置/文案，禁止假大空 UI 重做）

| 项 | 做法 | 一线参照 |
|----|------|----------|
| 开场白 | 已有则压测；弱则改：学科+课题+要下载 |
| 推荐问题 | 保留 ≥2 条可一点就 G1/G2 |
| 等待 | Dify 默认流式；若白屏过长，查工作流超时/节点 |
| 下载 | data-URL 可点；提示「点链接保存」 |
| 错误 | 限流/失败回复模板（工作流或提示词） |

**禁止：** 为「看起来像 GPT」加一堆不能点的装饰按钮。

### 3.3 证据

目录：`ops/evidence/p0-gold/`  
每条：`meta` 片段 + 产物样例（html/md/head）  
汇总：`ops/P0-GOLD-REPORT.md`

### 波 1 完成定义

```text
[ ] G1 G1+ G2 G3 全 PASS · 空成功 0
[ ] G4 至少 1 次诚实失败或说明「现网难复现」+ 话术已备
[ ] 证据进仓 + P0-GOLD-REPORT
[ ] 未关限流刷指标
[ ] RUNBOOK 波 1 勾满 + Issue
```

---

## 4. 波 2a · CLAIM-B（教师正式可用）

**前提：** 波 0 + 波 1 绿。  
**CLAIM-B 定义（钉死）：**  
非技术同事用**默认公开链接**，在**主流浏览器 + 手机**，无需运维陪同，完成「打开 → 要课件 → 下载 → 改一版」，且证书无警告、无空成功。

### 4.1 验收清单（产品）

| # | 项 | 过线 |
|---|-----|------|
| B1 | 桌面 Chrome/Edge 打开 | 无证书警告 |
| B2 | 手机 Safari/Chrome 4G | 同上 |
| B3 | 零培训完成 G1 | 有下载 |
| B4 | 同会话 G1+ | 有下载 |
| B5 | G3 大纲 | 无假文件 |
| B6 | 失败可理解 | 抽 1 次 |
| B7 | 话术包 | `ops/CLAIM-B-SCRIPT.md`（给老师 5 句） |
| B8 | **未**全校群发/收费承诺 | 纪律 |

### 4.2 明确不纳入 CLAIM-B

- full real 班级数据  
- Harness / 编码 Agent  
- 控制台能力暴露给老师  

### CLAIM-B 完成定义

```text
[ ] B1–B7 勾满 · 证据或截图路径进仓（无隐私）
[ ] PIN：CLAIM-B=YES
[ ] 正式上线 / 全校推广仍默认否（另授权）
[ ] Issue「CLAIM-B PASS」
```

---

## 5. 波 2b · FULL-REAL（edu live → CLAIM-C-REAL full）

**前提：** hybrid 已绿；**edu-core 提供只读白名单 API**（业主/对接方给基址与契约）。  
**可与 2a 并行**，但 **互不顶替 CLAIM**。

### 5.1 工作包（在 C-REAL-PACK 上升级）

| 步 | 内容 | 过线 |
|----|------|------|
| R0 | EDU-BRIDGE v0.3 · MODE=real · 白名单 path 钉死 | 书面 |
| R1 | 真 JWT/OIDC 或 edu 换票 | `/me` 真 school |
| R2 | 只读 live classes/courses | 非 fixture source |
| R3 | 跨校 403 · apply 仍 403 | smoke |
| R4 | Dify 工具改指 live | Chat 命中真数据 |
| R5 | Ce-R 全回归 + G1 不回归 | 全绿 |

### 5.2 禁止

- fixture 冒充 full real  
- Agent apply / 写成绩  
- 公网匿名 exchange  

### CLAIM-C-REAL full 完成定义

```text
[ ] MODE=real · PIN 升级
[ ] 只读 live 证据（脱敏）
[ ] smoke + Ce-R
[ ] 未自动 CLAIM-B（除非 2a 已过）
```

---

## 6. 角色与工期感（写实）

| 波 | 谁 | 量级 |
|----|-----|------|
| 0 | 运维 + 轻前端 | 0.5～2 天（卡 WAF 则拉长） |
| 1 | 运维/执行窗跑路径 + 可选提示词 | 0.5～1 天 |
| 2a | 产品 + 1 名真实用户眼 | 0.5 天 |
| 2b | 研发 + edu 对接 | 视 API 就绪 2～5 天+ |

---

## 7. 风险

| 风险 | 缓解 |
|------|------|
| 外网 TLS 仍 RST | 波 0 硬门；未过不刷 G 充数 |
| 把 Dify 壳当失败 | 文档钉：公开页=聊天出件 |
| 抢做 Harness | 本包明确不做 |
| 2b 无 API | 保持 hybrid；不假 full |
| E1 手工续期忘 | 波 0.2 强制策略 |

---

## 8. 关联文件

| 文件 | 用途 |
|------|------|
| `ops/P0-GATE-RUNBOOK.md` | 总勾选 |
| `ops/CLAIM-B-RUNBOOK.md` | 2a |
| `ops/FULL-REAL-RUNBOOK.md` | 2b |
| `ops/PHASE-C-REAL-PACK.md` | 2b 细节继承 |
| `ops/PHASE-E1-PACK.md` | 续期参考 |
| `ops/TASK-CARDS-P0-GATE.md` | 标准任务卡 |

---

## 9. 总出口（大包）

```text
P0-GATE 大包可报「阶段完成」当且仅当：
  波 0 PASS
  波 1 PASS（空成功 0）
且下列至少一条业主点名收口：
  2a CLAIM-B PASS  和/或  2b CLAIM-C-REAL full PASS
禁止用 hybrid 或 E1 单独冒充 CLAIM-B。
```
