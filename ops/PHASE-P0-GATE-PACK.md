# 任务包 · P0-GATE（一张卡做完）

```
STATUS: BINDING · 重新派发 · 单包单卡
DATE: 2026-08-06
CODE: PHASE-P0-GATE
形态: Dify Web + DeepSeek · 非 Harness
对标: 打开即用 · 过程可感 · 要文件有下载 · 失败诚实（一线 AI 站心智）
```

> **一个任务包，一张任务卡，一次回写收口。**  
> **禁止** 拆成多卡平行报绿；**禁止** 口头完毕；**禁止** 假 CLAIM-B / 假 full real。  
> **交付 =** 本 RUNBOOK 勾满 + 证据进仓 + PIN/CANON + Issue 回写 + push main。

---

## 1. 背景水位（勿重做）

**已收底盘：** A/B · C-hybrid · D-LITE · E1(LE)  
**本包要收：** 稳定可达 + 金路径体感（空成功 0）+ **CLAIM-B 产品验收**  
**本包顺带能做则做：** full real 仅当 edu API 已就绪；**未就绪则明确 NO，不挡 CLAIM-B**  
**不做：** OpenWork/Harness 主线 · Agent 写库 · 全校推广话术 · 密钥进仓

---

## 2. 包内工作（按序 · 同一执行窗一次做完）

### 段 A · 稳定（P0）

| # | 动作 | 过线 |
|---|------|------|
| A1 | 公网 `https://workbench.aivia.asia` TLS | 握手成功，非 connection reset（连测 ≥3） |
| A2 | 默认 Chat 桌面打开 | 首屏有「Aivia 课件」壳，无证书惊吓 |
| A3 | 手机 4G 打开同一链接 | 同上 |
| A4 | 证书续期策略书面 | 自动 dns_ali **或** 手工 TXT 步骤写在 RUNBOOK 备注 |
| A5 | 真源去滞后 | README/CANON 与 PIN 一致（E1 PASS，无「仍自签/E1 BLOCKED」） |
| A6 | bridge | health 200 · 非公网匿名 exchange |

**A 不过：** 允许记 BLOCKED 原因并停；**不得**用金路径刷数冒充稳定。

### 段 B · 金路径体感（对标一线出件）

入口：`https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl`  
证据目录：`ops/evidence/p0-gate/`

| ID | 用户怎么说 | 过线 |
|----|------------|------|
| **G1** | 做×× HTML 课件，要能下载 | DOWNLOAD_READY + 真 HTML 可开有标题 |
| **G1+** | 同会话改一版加练习 | 仍有可下载文件 |
| **G2** | ××教案可下载 | 文件可下（md 可） |
| **G3** | 只要大纲不要文件 | **无**假 DOWNLOAD_READY |
| **G4** | 失败/限流或难需求 | 人话失败，不装成功（难复现则写说明+话术） |

**空成功次数必须 = 0**（要文件却无文件 = 失败）。  
可选：收紧开场白/推荐问题文案；**禁止**堆不能点的装饰控件。

### 段 C · CLAIM-B（教师正式可用）

**定义：** 非运维人员用默认公开链接，在桌面 + 手机完成打开→要课件→下载→改稿；证书无警告；无空成功。  
**≠** 全校上线 · **≠** full real · **≠** 控制台能力。

| # | 项 |
|---|-----|
| C1 | 桌面无证书警告 + G1 过 |
| C2 | 手机 4G 无证书警告 + 能聊 |
| C3 | G1+ 改稿过 |
| C4 | G3 无假文件 |
| C5 | 老师五句话术 → `ops/CLAIM-B-SCRIPT.md` |
| C6 | PIN 写 `CLAIM-B=YES`；**正式上线仍默认否** |

### 段 D · full real（可选 · 有 API 才做）

| 条件 | 动作 |
|------|------|
| edu 只读 API **未就绪** | RUNBOOK 勾「D 跳过 · 保持 hybrid」· **不**报 full real |
| **已就绪** | MODE=real · live classes · 跨校 403 · Dify 工具命中 · PIN full · 脱敏证据 |

---

## 3. 完成定义（整包唯一 CLAIM 口）

```text
P0-GATE 整包 PASS 当且仅当：
  [ ] 段 A 全过（或 A 仅续期手工策略但 TLS/打开全过）
  [ ] 段 B：G1/G1+/G2/G3 PASS · 空成功 0 · 证据在 ops/evidence/p0-gate/
  [ ] 段 C：CLAIM-B=YES 已写入 PIN · SCRIPT 已进仓
  [ ] 段 D：跳过已声明 或 full real 已绿
  [ ] ops/P0-GATE-RUNBOOK.md 填满
  [ ] 短报告 ops/P0-GATE-REPORT.md（结论+空成功0+CLAIM-B+正式上线否）
  [ ] CANON/HANDOFF/README/DEBT 一句同步
  [ ] Issue #1 回写「P0-GATE PASS」+ push main

禁止：
  - 只做 A 或只做 B 报整包完
  - E1/hybrid 冒充 CLAIM-B
  - 正式全校上线未授权却宣传
```

---

## 4. 风险与对标

| 风险 | 缓解 |
|------|------|
| 外网 TLS RST | A 硬门 |
| 模型波动空成功 | B 计 0；失败重跑记次数 |
| 公开页不像控制台 | 文档钉：聊天出件即产品 |
| 抢做 Harness | 包外 |

---

## 5. 关联

- 勾选：`ops/P0-GATE-RUNBOOK.md`  
- **唯一任务卡：** `ops/TASK-CARD-P0-GATE.md`  
- 入口 Chat 如上  
