# 任务包 · WB-ALIGN（全面对标实现 · 完整无人值守）

```
STATUS: BINDING · 单包单卡 · 分阶段自审自修
DATE: 2026-08-06
CODE: PHASE-WB-ALIGN
前提: CLAIM-WB-SURVEY=YES · MATRIX 为范围真源
执行窗: 本机 Grok（可 SSH 云端）· 可本机浏览器/Office 验收
模式: 全程无人参与——每阶段结束必须自审；不达标则本阶段修复循环，禁止跳阶段假绿
```

> **一张完整任务卡覆盖「按 WorkBuddy 对标矩阵把该有的能力做齐」。**  
> 名字可与 WB 不同；**用户前台 vs 管理员后台** 分流；clean-room，不拆闭源、不抄像素。  
> **内容主靠模型 API；壳/治理/下载/组织** 按矩阵补齐。  
> **禁止** 空成功、data-URL 主路径、`[blocked]`、口头完毕、假全校上线、密钥进仓、Agent 写库。

---

## 0. 总目标与完成定义（整包唯一 CLAIM）

### 0.1 目标

在 Aivia（Web + Dify + DeepSeek + bridge `/dl`）上，按  
[`ops/WB-FEATURE-MATRIX.md`](./WB-FEATURE-MATRIX.md)  
将 **P0+P1 优先级** 能力做到 **可验收的高标准**；P2/后置项必须在终报告中 **显式声明跳过原因**（生态/桌面/法律），不得装成已做。

### 0.2 CLAIM-WB-ALIGN 整包过线（缺一不可）

```text
[ ] 阶段 S0–S5 各自 GATE 自审 PASS 文件存在且勾满
[ ] 矩阵勾选：所有标 P0 的 ID = 有（或「等价实现」写清映射）
[ ] 矩阵勾选：所有标 P1 的 ID = 有 或 书面 BLOCKED+业主可接受理由（默认要求有）
[ ] 用户主路径：SCENE-FULL S1–S8 回归空成功0 · /dl 无 blocked · 本机打开
[ ] 管理能力：G-03 审计 · G-05 写库门禁 · G-07 配额/限流可运营 · G-13 空成功/失败可观测 —— 均有证据
[ ] 终报告 ops/WB-ALIGN-REPORT.md + 证据树 ops/evidence/wb-align/
[ ] PIN/CANON：CLAIM-WB-ALIGN=YES · 正式上线仍否（除非另授权）
[ ] Issue 最终回写 + push main
[ ] 无密钥 · 无逆向 · 无「已1:1复制 WorkBuddy」表述
```

**高标准含义：**  
- 验收以 **真人浏览器路径** 为准（本机），API 绿只算辅助。  
- 管理项以 **可操作的配置/日志/脚本/面板** 为准，文档空话不算。  
- 每阶段自审表 **不达标 → 修到过线**，禁止带已知 FAIL 进下一阶段。

---

## 1. 无人值守运行协议（BINDING）

```text
for stage in S0..S5:
  执行本阶段「做」
  跑本阶段「自审清单」→ 写入 ops/evidence/wb-align/gate-S{n}.md
  if 任一条 FAIL:
      修复（最多记录 3 轮 fix-log）
      重新自审
      if 仍 FAIL: 整包 CLAIM-WB-ALIGN=BLOCKED，写清阻塞，停止（勿假绿后续阶段）
  else:
      标记 stage PASS，自动进入下一阶段
全部 PASS → 终自审 S-FINAL → 回写 CLAIM
```

| 规则 | 要求 |
|------|------|
| 无人参与 | 不中途问业主「能不能过」；只在 **整包结束或 BLOCKED** 回写 Issue |
| 自审 | 每阶段固定清单，可勾选、可复现 |
| 修复 | 同阶段内完成；禁止「已知坏下载还去做专家目录」 |
| 证据 | 每阶段至少 1 个证据目录 `ops/evidence/wb-align/S{n}/` |
| 执行窗 | **本机 + SSH 云端**；改现网配置必须 SSH；点验必须本机浏览器 |

---

## 2. 范围真源

| 文档 | 用途 |
|------|------|
| `ops/WB-FEATURE-MATRIX.md` | 能力 ID 与优先级 |
| `ops/WB-SURVEY-REPORT.md` | 分期建议与红线 |
| `ops/WB-ORG-MODEL.md` | 前台/后台分流 |
| `ops/WB-RESPONSE-LOGIC.md` | 完成态/产物行为对标 |
| CANON | 不写库、/dl 主路径、正式上线默认否 |

**实现原则：**

1. Chat = 任务对话 + 交付；**治理不进老师按钮墙**。  
2. 管理能力 → Dify Console + bridge + `ops/` 脚本/轻面板 + 日志。  
3. 下载主路径保持 `https://workbench.aivia.asia/dl/...`。  
4. 桌面本地盘、企微全量、像素抄 UI = 后置/不做（终报告声明）。

---

## 3. 阶段定义（S0→S5 自动串行）

### 阶段 S0 · 底盘冻结与回归门（守住已有）

**目的：** 对标扩建前先保证不回退。

| 做 | 验收标准（高） |
|----|----------------|
| 确认 BASE Chat 与 `/dl` | 抽样 1 链 GET 200 + `Content-Disposition: attachment` |
| 回归 SCENE-FULL 要点 | S1 HTML · S3 XLSX · S4 大纲无假文件 · S6 拒写库 · S8 无 blocked |
| 空成功 | **0** |
| 本机打开 | HTML 浏览器 / XLSX Excel|WPS 至少各 1 |

**自审 gate-S0.md 必填：** 上表全 PASS 或 FAIL+修复记录。  
**FAIL 例：** 再出现 `[blocked]` 或 data-URL 主路径。

---

### 阶段 S1 · 管理 P0（运营可观测与安全）——矩阵 G 优先

对应 MATRIX（至少）：**G-03 审计 · G-05 写库门禁 · G-07 配额/限流 · G-13 空成功/失败监控**。  
可合并实现，但 **四条各自可演示**。

| ID | 能力（Aivia 拟名） | 高标准验收 |
|----|-------------------|------------|
| G-07 | 配额/日限额/限流可配 | 有配置位（env/nginx/Dify/ops 文档三选一以上落地）+ **触发一次可见限制或指标** 的证据 |
| G-13 | 空成功/失败监控 | 有日志或报表：统计「要文件无文件」/失败码；跑 1 次注入或回放能看到计数变化 |
| G-03 | 审计 | 会话/下载/关键工具 关键关键至少两类写入审计介质（文件/DB）；样例日志进 evidence（脱敏） |
| G-05 | 写库门禁策略化 | 拒写成绩库 **策略可指出配置/提示词/桥**；换说法再拒 1 次；无假成功 |

**自审 gate-S1.md：** 四 ID 全 PASS。  
**禁止：** 只写 Markdown「应该限流」无现网行为。

---

### 阶段 S2 · 用户交付壳（对标完成态/产物）

对应至少：**B-09 产物面板或等价索引 · A-08 运行摘要（可简化）· B-07 下载稳定 · 回归 DOC 格式**。

| ID | 高标准验收 |
|----|------------|
| B-07 | 连续 HTML/XLSX/DOCX 各 1 次：`/dl` 链、无 blocked、本机打开 |
| B-09 | 用户能在界面看到 **可点产物列表或稳定下载区**（非仅靠翻聊天找 data）；截图证据 |
| A-08 | 任务结束可见 **耗时或状态摘要**（Dify 原生进度可接受，须说明等价） |
| B-01/02/05 | DOCX/XLSX/HTML 仍绿（抽测） |

**自审 gate-S2.md** 全过才进 S3。

---

### 阶段 S3 · 用户输入与场景组织（对标 Composer/chip）

对应至少：**A-06 场景结构化 · A-07 组合输入（文件优先）· C-01 上传再加工 · C-04 模板入口**。

| ID | 高标准验收 |
|----|------------|
| A-06 | ≥4 类场景入口（推荐问题/芯片/菜单），点后能启动对应意图 |
| A-07 / C-01 | 用户可 **上传文件** 并基于文件出可下载产物 1 次（fixture 文件可） |
| C-04 | 至少 2 个可复用模板/结构（课件/教案/表）可从入口触发 |
| 防串台 | 连续 课→表→大纲 类型正确（SCENE S7 再跑） |

**自审 gate-S3.md**。

---

### 阶段 S4 · 矩阵 P1 补齐与诚实跳过

| 做 | 验收 |
|----|------|
| 遍历 MATRIX 全部 **P1** 行 | 每行：`有` / `等价有（说明）` / `本包跳过（原因）` 写入 `ops/WB-ALIGN-MATRIX-STATUS.md` |
| 能做的 P1（如 B-03 PPT 可用 HTML 幻灯片等价、D-01 联网说明、E 多应用入口） | 做到可演示或写清等价 |
| P2/后置（桌面 C-02、IM H、企业知识乐享…） | **必须** 跳过表，禁止标「有」 |
| 教育 I 域 | 保持拒写库；full real 未就绪则 I-06 跳过 |

**自审 gate-S4.md：** 无「静默空洞」（每个 P0/P1 ID 有状态）。

---

### 阶段 S5 · 全量回归 + 终自审 + 回写

| 做 | 验收 |
|----|------|
| 用户金路径电池 | SCENE S1–S8 思想再跑；空成功 0；/dl 主路径 |
| 管理四件套抽检 | G-03/05/07/13 各 1 证据仍有效 |
| 安全 | 无密钥进仓；bridge 非公网裸 exchange |
| 文档 | `WB-ALIGN-REPORT.md` 含：做了什么、矩阵状态摘要、跳过项、如何验收、已知限制 |
| 真源 | PIN/CANON/HANDOFF/README/DEBT |
| Issue | 最终「CLAIM-WB-ALIGN PASS\|BLOCKED」 |

**gate-S-FINAL.md** 通过 → 才允许 `CLAIM-WB-ALIGN=YES`。

---

## 4. 每阶段自审模板（强制复制到 gate 文件）

```markdown
# gate-S{n}
DATE: ...
STAGE: S{n}
RESULT: PASS | FAIL

## 清单
| # | 标准 | 结果 | 证据路径 |
|---|------|------|----------|
| 1 | ... | PASS/FAIL | ... |

## 若 FAIL
- 现象:
- 修复动作:
- 重测结果:

## 空成功计数: 0
## data-URL 主路径: 否
## 密钥进仓: 否
```

---

## 5. 证据与回写目录

```text
ops/evidence/wb-align/
  gate-S0.md ... gate-S5.md · gate-S-FINAL.md
  S0/ S1/ S2/ S3/ S4/ S5/
ops/WB-ALIGN-MATRIX-STATUS.md
ops/WB-ALIGN-REPORT.md
ops/WB-ALIGN-RUNBOOK.md   # 总勾选
```

---

## 6. 红线

- 拆 WorkBuddy 闭源 / 像素抄 UI  
- 无 MATRIX 状态表声称「全有」  
- 管理能力只做前台花活  
- 跳过自审进下一阶段  
- 正式全校上线未授权却宣传  
- Agent 直写成绩库  

---

## 7. 关联

- **唯一任务卡：** `ops/TASK-CARD-WB-ALIGN.md`  
- 勾选总表：`ops/WB-ALIGN-RUNBOOK.md`  
- 调查真源：MATRIX / SURVEY-REPORT / ORG / RESPONSE-LOGIC  
