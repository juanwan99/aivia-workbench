# 任务包 · DOC-SOLID（文档/报表做扎实）

```
STATUS: PASS · CLAIM-DOC-SOLID=YES · 正式上线=否
DATE: 2026-08-06
CODE: PHASE-DOC-SOLID
前提: P0-GATE PASS · CLAIM-B=YES · 正式上线=否 · hybrid
形态: Dify Web + DeepSeek · clean-room 对标 WorkBuddy 行为（不拆闭源）
方式: 云端改工作流/节点/模板 → 本地浏览器真点真下真开文件 → 证据进仓
出口: ops/DOC-SOLID-REPORT.md · ops/evidence/doc-solid/
```

> **一个任务包 · 一张任务卡 · 一次回写收口。**  
> **禁止** 空成功、口头完毕、假「已全面对标 WorkBuddy」、未授权全校上线、Agent 写库、密钥进仓。  
> **交付 =** RUNBOOK 勾满 + 本地可开产物进仓 + 短报告 + PIN/CANON 一句 + Issue + push。

---

## 0. 产品目标（对标一线行为，不是换壳）

| WorkBuddy 类体感 | 本包必须 |
|------------------|----------|
| 说要文档/表就有真文件 | MIME 正确、本机 Word/WPS/Excel 能打开 |
| 多轮改一版仍出件 | 同会话改标题/加列/加练习 |
| 不要文件就不装样 | 只要大纲 → 无假下载 |
| 失败诚实 | 超范围/写库 → 人话拒绝 |
| 流畅 | 默认链可完成；不依赖运维陪同点控制台 |

**不做本包：** OpenWork 主线、Codex/OpenCode Harness、OnlyOffice 精修、全格式一次上齐、full real 假绿。

---

## 1. 范围钉死（串行 · 避免十种格式并行）

| 优先级 | 格式 | 最低故事 |
|--------|------|----------|
| **P0 必做** | **XLSX 报表** | 「做一份××周/班 统计表，要能下载 Excel」→ 本机 Excel/WPS 打开有表头+≥3 行数据 |
| **P0 必做** | **DOCX 或可互操作的教案文档** | 优先真 **DOCX**；若现网节点受限，允许 **MD 下载 + 书面说明** 并开 ISSUE 记 DOCX 技术债，但 **XLSX 不可用 MD 替代** |
| **P1 保持** | HTML 课件 / MD | 回归 G1/G1+ 不回退（空成功 0） |
| **数据** | 第一期 | **模板/合成数据** 即可；不挡包。真数等 full real |

默认 Chat：`https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl`  
若需新应用/工作流：可新建并 **改 README/PIN 默认入口**（禁止 silently 双主入口）。

---

## 2. 工作段（同一卡按序）

### 段 S0 · 开工钉死（≤1h）

- [ ] 确认执行窗：**可本地浏览器测** + **可改 Dify/仓**  
- [ ] 打开默认链，冷启动有壳  
- [ ] 记下当前工作流：出件方式（data-URL / 文件节点 / 其他）  
- [ ] 本包 MODE 数据：`fixture`（合成表数据）  

### 段 S1 · XLSX 报表链路（核心）

| # | 动作 | 本地过线 |
|---|------|----------|
| S1.1 | 工作流/Code 节点生成 **真 xlsx**（非改后缀的假文件） | `file` 命令或 Excel 打开 |
| S1.2 | 用户话术触发下载 | DOWNLOAD_READY 或等价可点下载 |
| S1.3 | 表头 + ≥3 行 + 可读中文 | 本地打开目视 |
| S1.4 | 同会话改表（加一列或改标题）再下 | 新文件内容变化 |
| S1.5 | 证据 | `ops/evidence/doc-solid/s1-*.xlsx` + meta |

### 段 S2 · 文档（DOCX 优先）

| # | 动作 | 过线 |
|---|------|------|
| S2.1 | 教案/报告 **DOCX** 可下可开 | 本地 WPS/Word |
| S2.2 | 若 DOCX 技术挡板 | MD 可下 + `ops/evidence/doc-solid/docx-debt.md` 写清原因与下一刀；**不**报「DOCX 已满绿」 |
| S2.3 | 同会话改一版 | 新文件 |

### 段 S3 · 回归与诚实

| ID | 过线 |
|----|------|
| R-G1 | HTML 课件仍可下 · 空成功 0 |
| R-G3 | 只要大纲 · 无假文件 |
| R-G4 | 要求写成绩库 · 人话拒绝 |
| R-X | XLSX 路径再跑 1 次 PASS |

### 段 S4 · 体感（薄）

- 开场白/推荐问题增加 **「要 Excel 表」「要 Word 教案」** 各 ≥1  
- 失败/限流人话不回退  
- **禁止** 堆不能点的装饰按钮充「像 WorkBuddy」  

### 段 S5 · 回写收口

- RUNBOOK · 短报告 · PIN 一句 · Issue · push  
- CLAIM 名：`CLAIM-DOC-SOLID`（见下）  
- **正式上线仍否**  

---

## 3. 本地测试协议（强制 · 执行窗自备浏览器）

每条 S1/S2/R-*：

1. 本地打开默认链（或 PIN 新入口）  
2. 真人话发送（可用 SCRIPT 扩写）  
3. 下载到本地目录  
4. **用系统应用打开**（Excel/WPS/浏览器）  
5. 截图可选；**产物文件必须进仓**（xlsx/docx/md/html）  
6. 记耗时；>90s 写备注  

服务器 API 烟测可辅助，**不能替代** 本地打开。

---

## 4. CLAIM-DOC-SOLID 完成定义

```text
[ ] S1 XLSX：可下 + 本地 Excel/WPS 能开 + 改稿再下
[ ] S2 DOCX 满绿 或（MD 替代 + docx-debt 书面）——二选一诚实
[ ] S3：R-G1/R-G3/R-G4/R-X 空成功 0
[ ] S4：推荐问题含表/文档
[ ] 证据 ops/evidence/doc-solid/ + DOC-SOLID-REPORT.md
[ ] RUNBOOK 填满 + PIN/CANON + Issue + push
[ ] 未勾正式上线 · 未假 full real · 未上 Harness 主线

CLAIM-DOC-SOLID = 文档/报表交付扎实（表硬 + 文档路径诚实）
≠ WorkBuddy 全量功能复制
≠ 全校上线
```

---

## 5. 风险

| 风险 | 缓解 |
|------|------|
| Dify 仅易出 HTML/MD | Code 节点生成 xlsx（openpyxl 等）或官方文件工具；密钥不进仓 |
| data-URL 过大 | 改文件存储/短链；报告记录方案 |
| 本地窗与云端不一致 | 同一 BASE URL；改入口必改 PIN |
| 范围膨胀 PPT/PDF 全上 | 本包只钉 XLSX + DOCX/MD |

---

## 6. 关联

| 文件 | 用途 |
|------|------|
| `ops/DOC-SOLID-RUNBOOK.md` | 勾选 |
| `ops/TASK-CARD-DOC-SOLID.md` | **唯一任务卡** |
| `ops/CLAIM-B-SCRIPT.md` | 可扩展表/文档句 |
| 默认 Chat | 见 PIN |
