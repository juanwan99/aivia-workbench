# 任务包 · SCENE-FULL（个人全场景打通 · 对标 WorkBuddy 行为）

```
STATUS: PASS · CLAIM-SCENE-FULL=YES · 正式上线=否
DATE: 2026-08-06
CODE: PHASE-SCENE-FULL
前提: CLAIM-B · DOC-SOLID · DL-FIX(/dl https) · 正式上线=否
口径: 内容主靠 DeepSeek API/模型；产品只保证「各场景能要到、能下、能开、能改、失败诚实」
对标: WorkBuddy 行为 clean-room（不拆闭源、不宣称 1:1 抄功能）
出口: ops/SCENE-FULL-REPORT.md · ops/evidence/scene-full/
```

> **一个任务包 · 一张任务卡 · 一次回写收口。**  
> **禁止** 空成功、data-URL 主路径、`[blocked]` 报绿、口头完毕、假全校上线、Agent 写库、密钥进仓。  
> **交付 =** 场景矩阵勾满 + 本地真下真开 + 证据/报告 + PIN/CANON + Issue + push。

---

## 0. 产品口径（绑定）

| 层 | 谁负责 |
|----|--------|
| 写什么、改什么、表意/结构 | **模型 API**（DeepSeek） |
| 聊天入口、意图不丢、https 下载、真文件可开、多场景不串 | **工作台产品**（Dify 应用 + `/dl` + 提示/路由） |
| 真学校库 | 非本包必做（fixture 即可；full real 另卡） |

本包目标：

> **个人日常换场景、换说法，默认链上都能正常完成**（对标 WorkBuddy「换活也能干」的行为，不是重造模型）。

---

## 1. 场景矩阵 P0（本包必绿）

入口：`https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl`（改入口必写 PIN）  
下载主路径：**仅** `https://workbench.aivia.asia/dl/...`（PHASE-DL-FIX）  
每格过线：**3 种说法至少 2 种 PASS** + **可下（无 blocked）** + **本机打开** + **空成功 0**

| ID | 场景 | 用户意图 | 产物 | 加深 |
|----|------|----------|------|------|
| **S1** | HTML 课件 | 学科+课题要课件 | `.html` via `/dl` | 2 学科说法 |
| **S2** | Word 教案 | 一课时教案 | `.docx` via `/dl` | 改一版加练习 |
| **S3** | Excel 表 | 统计/登记/提交表 | `.xlsx` via `/dl` | 改一版加列或改标题 |
| **S4** | 只要大纲 | 明确不要文件 | **无** DOWNLOAD 假绿 | 口语「别下文件」 |
| **S5** | 同会话改稿 | 基于上一版改 | 新 `/dl` 文件 | 与 S1/S2/S3 之一绑定 |
| **S6** | 拒做写库 | 要写成绩/教务库 | 人话拒绝 · 无假成功 | 换一种违法/越权说法亦可 |
| **S7** | 连续切换 | 连做 课件→表→大纲 三次 | 三次各自正确 | 防串台（表里不当课件下） |
| **S8** | 下载手感 | 点链接 | 浏览器开始下载 · **无 [blocked]** | Chrome 或 Edge 至少 1 |

**P1（本包能做则做，不挡 CLAIM；做不完写债）：**  
手机下载 1 次 · 稍大表人话上限 · 周报/通知短文 MD 或 DOCX。

**P2 明确不做：** PPT 全家桶、Harness、OpenWork 主线、全校上线、假 full real。

---

## 2. 工作段（单卡按序）

### F0 · 钉口径与基线（≤1h）

- [ ] 确认 `/dl` 仍主路径（抽 1 次 HTML 链含 `workbench.../dl/`）  
- [ ] 确认非 data-URL 主路径  
- [ ] 场景矩阵表进 RUNBOOK  
- [ ] 数据 MODE=fixture  

### F1 · 内容场景（模型为主 · 提示/推荐补齐）

- [ ] 推荐问题覆盖：课件 / Word / Excel / 大纲  
- [ ] 系统提示：意图识别（课件|教案|表|大纲|拒写库）；出件必须走 PackDownload→`/dl`  
- [ ] 跑 S1–S4 矩阵（多说法）  

### F2 · 交付与多轮（产品壳）

- [ ] S5 改稿  
- [ ] S6 拒做  
- [ ] S7 连续三任务  
- [ ] S8 浏览器点下无 blocked  

### F3 · 回归与债

- [ ] 空成功总计 0  
- [ ] 失败格子写入 `ops/evidence/scene-full/debts.md`（有则）  
- [ ] P1 项做或声明跳过  

### F4 · 回写

- [ ] `ops/SCENE-FULL-REPORT.md`  
- [ ] 证据 `ops/evidence/scene-full/`（每主场景 ≥1 产物或 head）  
- [ ] PIN：`CLAIM-SCENE-FULL=YES` 或 BLOCKED 原因  
- [ ] CANON/HANDOFF/README · Issue · push  

---

## 3. 本地测强制（个人使用视角）

每条 S1/S2/S3/S5/S8：

1. 真人打开默认链  
2. 打字或点推荐  
3. 点 **https /dl** 下载（记录有无 `[blocked]`）  
4. 本机浏览器 / Excel / Word|WPS 打开  
5. 文件进仓  

**禁止** 仅 API 拆包报「全场景通」。

---

## 4. CLAIM-SCENE-FULL 完成定义

```text
[ ] S1–S8 全 PASS（S7 连续三任务正确；S8 无 blocked）
[ ] 下载主路径仍为 https /dl（无 data-URL 主路径）
[ ] 空成功 = 0
[ ] 证据 + SCENE-FULL-REPORT + RUNBOOK 填满
[ ] PIN/CANON + Issue + push
[ ] 正式上线=否 · 未假 WorkBuddy 1:1 · 未假 full real

CLAIM-SCENE-FULL = 个人全场景（P0 矩阵）打通
≠ 全校上线
≠ WorkBuddy 功能复制完成
≠ 模型重训
```

---

## 5. 风险

| 风险 | 缓解 |
|------|------|
| 模型波动 | 同场景 2 说法；失败记债不硬刷关限流 |
| 串台 | S7 门禁；提示词强调当前任务类型 |
| 下载回退 data-URL | F0/S8 死查；发现即 FAIL |
| 范围膨胀 PPT/真数 | P2 禁；债另列 |

---

## 6. 关联

- 勾选：`ops/SCENE-FULL-RUNBOOK.md`  
- **唯一任务卡：** `ops/TASK-CARD-SCENE-FULL.md`  
- 依赖：DL-FIX `/dl` · DOC-SOLID 格式能力 · CLAIM-B 入口  
