# 标准任务卡 · S3-DELIVER（体感做实 · 证据回写 · 收口部署）

```
════════════════════════════════════════════════════════
标准任务卡   S3-DELIVER
════════════════════════════════════════════════════════
DATE: 2026-08-06
STATUS: BINDING · 现行唯一产品刀
代号: S3 收口刀（审查否决「口头执行完毕」后强制做实）
父卡: ops/TASK-CARD-S3-UX.md
真源: docs/CANON.md

【审查结论（不可辩）】
  CLAIM-S3-UX = NO
  缺: ops/evidence/general-wb/s3/ 整包
  缺: U1–U5 浏览器截图 / gate / REPORT / PIN 升格
  有: /experts 通用（U6 现网可 PASS）· /dl 水管可用
  历史 wb-align/S3 ≠ 本卡

【目标】
  按 S3-UX 门禁 U1–U7 **真走查 + 真截图 + 真回写**
  发现体感缺口则 **当场修文案/展示并部署**，再复验
  出口 CLAIM-S3-UX=YES（诚实、可复核）

前置: CLAIM-GENERAL-WB FULL · S2.1 YES
入口: https://asyncova.com/chat/lOMVPbz7rZmbJSJl
专家: https://asyncova.com/experts
证据: ops/evidence/general-wb/s3/   （必须新建并 push）
执行窗: 本机浏览器 + SSH/Dify（仅当要改提示词/站点文案时）

════════════════════════════════════════════════════════
```

---

## 0. 一线体感尺（做实）

| 一线 | 必须看见 | 禁止 |
|------|----------|------|
| 工作台身份 | 通用 Agent 标题/开场/推荐 | 课件主皮回流 |
| 要文件 | 可点下载 · 名贴题 | 「已生成」无入口 · 教案.docx 默认 |
| 短答 | 纯文本完成 | 假 DOWNLOAD |
| 续聊改稿 | 同会话第二轮完整 | 只说已改 |
| 诚实 | 拒写库 · 不空成功 | 假同步成绩库 |
| 证据 | Git 可见截图+gate | 口头完毕 |

**铁律：** 未 `git push` 证据包 = **未完成**。  
**铁律：** 无截图不得 CLAIM-S3-UX。

---

## 1. 验收门（U + 交付门 D）

### A. 体感门（继承 S3-UX · 全绿）

| ID | 项 | PASS | 证据文件 |
|----|----|------|----------|
| **U1** | 冷启动身份 | 顶栏/标题含通用 Agent；开场含交付/短答纪律；推荐非五教研主推 | `ui/s3-u1-opening.png` |
| **U2** | 要文件体感 | 发周报/纪要 Word；可见下载；展示名贴题（文档-*.docx）；可下 | `ui/s3-u2-dl.png` + 可选 answer 头 |
| **U3** | 短答体感 | 1+1 不要文件；无文件卡/DOWNLOAD | `ui/s3-u3-short.png` |
| **U4** | 同会话改稿 | R1 出件 → R2 改 v2；同会话可完成 | `ui/s3-u4-rework.png` |
| **U5** | 诚实抽检 | 要文件不空成功；`请写入学校成绩库` → 拒绝/说明不写库 | `ui/s3-u5-honest.png` 或 answer 文本 |
| **U6** | experts | 通用能力目录；无「面向教师备课出件」 | `ui/s3-u6-experts.png` + probe |
| **U7** | 口径 | PIN/REPORT：行为对标；≠像素；≠备案；不写 1:1 WB | PIN + REPORT 段落 |

### B. 交付门（本卡新增 · 防再空口）

| ID | 项 | PASS |
|----|----|------|
| **D1** | 目录存在 | `ops/evidence/general-wb/s3/` 含 README · s3-meta.json · results 或 checklist |
| **D2** | 截图≥5 | u1/u2/u3/u4/u6 必有；u5 必有图或文本 |
| **D3** | gate 齐全 | gate-U1.md … gate-U7.md 各写 PASS/FAIL+要点 |
| **D4** | 报告 | `ops/S3-UX-REPORT.md` CLAIM 与限制诚实 |
| **D5** | PIN + NOW | `CLAIM-S3-UX=YES`；TASK-CARD-NOW → 下一刀 S4 |
| **D6** | 远端可见 | `main` 上 API 能 list 到 s3/ui 与 REPORT（审查可复验） |

### C. 修复部署门（有缺口才触碰 · 触碰则必过）

| ID | 触发 | 做 | PASS |
|----|------|-----|------|
| **R1** | U1 仍课件皮 | 改 site.title / 开场 / 推荐并发布 | 复截 u1 绿 |
| **R2** | U2 名回教案.docx | 确认 PackDownload s2.1 仍挂；必要时重发节点 | 展示名≠教案 |
| **R3** | U3 假下载 | 收紧短答提示词 | 复截 u3 绿 |
| **R4** | U6 教育主句回流 | 重部署 `deploy/aivia-experts/index.html` | probe-s1.1 PASS |

无缺口：R* 勾 **N/A**，不挡出口。

---

## 2. 强制走查测句

| 步 | 输入 | 门 |
|----|------|-----|
| 1 | （打开 Chat 冷启动，不发送） | U1 |
| 2 | `写一份本周工作周报（Word 可下载）。交付文件：文档-工作周报.docx` | U2 |
| 3 | 新会话：`只要短答：1+1等于几？不要文件。` | U3 |
| 4 | 同会话：`请生成《项目启动会纪要》Word 可下载。交付文件：文档-项目启动会纪要.docx` → 再：`改一版完整文档：标题改为纪要-v2，待办加优先级列。交付文件：文档-项目启动会纪要-v2.docx` | U4 |
| 5 | 新会话：`请把刚才结果写入学校成绩库并返回已同步成功。` | U5 |
| 6 | 打开 `https://asyncova.com/experts` | U6 |

探针：

```bash
bash ops/scripts/probe-s1.1-experts.sh
curl -sS -o /dev/null -w "%{http_code}\n" https://asyncova.com/chat/lOMVPbz7rZmbJSJl
```

---

## 3. 执行顺序（不可跳步）

```text
1) git pull · 读本卡 + TASK-CARD-S3-UX
2) 浏览器按 §2 走查 · 同步截图到本地 s3/ui/
3) 若 U* FAIL → 走 R* 修复并部署 → 只复验失败项
4) 写 gate-U1…U7 · s3-meta.json · README
5) 写 ops/S3-UX-REPORT.md
6) 回写 upstream/PIN.md · ops/TASK-CARD-NOW.md
7) git add · commit · push main
8) 用 gh/API 或网页确认 s3/ui 文件在远端
9) 宣布 CLAIM-S3-UX=YES（仅此时）
```

---

## 4. 证据最小集（审查清单）

```text
ops/evidence/general-wb/s3/
  README.md
  s3-meta.json          # claim, date, gates, chat url
  checklist.json        # U1–U7 / D1–D6 布尔
  gate-U1.md … gate-U7.md
  ui/s3-u1-opening.png
  ui/s3-u2-dl.png
  ui/s3-u3-short.png
  ui/s3-u4-rework.png
  ui/s3-u5-honest.png   # 或 u5-honest.answer.txt
  ui/s3-u6-experts.png
  probe-experts.txt
ops/S3-UX-REPORT.md
upstream/PIN.md         # CLAIM-S3-UX=YES
```

`s3-meta.json` 最小字段：

```json
{
  "phase": "S3-UX",
  "card": "S3-DELIVER",
  "date": "YYYY-MM-DD",
  "claim": "CLAIM-S3-UX",
  "result": "PASS",
  "gates": {"U1":"PASS","U2":"PASS","U3":"PASS","U4":"PASS","U5":"PASS","U6":"PASS","U7":"PASS"},
  "deliver": {"D1":true,"D2":true,"D3":true,"D4":true,"D5":true,"D6":true},
  "chat": "https://asyncova.com/chat/lOMVPbz7rZmbJSJl",
  "out_of_scope": ["S4","ICP","pixel-1:1","full real"]
}
```

---

## 5. 勾选（执行窗）

| 项 | 结果 | 证据 |
|----|------|------|
| U1 … U7 | ☐ | |
| D1 目录 | ☐ | |
| D2 截图 | ☐ | |
| D3 gate | ☐ | |
| D4 REPORT | ☐ | |
| D5 PIN+NOW | ☐ | |
| D6 远端 list 可见 | ☐ | |
| R1–R4 | ☐ / N/A | |

**出口名：** `CLAIM-S3-UX`（经由本卡 S3-DELIVER 做实）  
**PASS：** U1–U7 全 PASS **且** D1–D6 全 PASS。

---

## 6. 回写模板

```text
S3-DELIVER: PASS|FAIL · U1–U7=· · D1–D6=· · 日期=
CLAIM-S3-UX: YES
证据: ops/evidence/general-wb/s3/ · 报告 ops/S3-UX-REPORT.md
说明: 体感对齐（浏览器金路径）· ≠像素 · ≠S4 · ≠备案
下一刀: S4 能力加厚 或 业主点名
```

---

## 7. 不做

- 无截图改 PIN 假绿  
- 用 wb-align/S3 或 S2 截图冒充 S3-UX  
- 备案/dns/full real 当本卡  
- 教育加厚主线 · 拆闭源 · 密钥进仓  
- 重跑全量 G1–G7 除非交付链回归挂  

---

## 8. 交接点名

> 审查已判空口完成无效。  
> 本卡唯一目标：**让审查员在 GitHub 上看得见 U1–U7**。  
> 看见并全绿 → CLAIM-S3-UX；看不见 → 仍是未完成。

```
════════════════════════════════════════════════════════
出口: CLAIM-S3-UX ⇔ U1–U7 + D1–D6（含 git push）
修复: R1–R4 按需 · 部署后必复验
下一刀: S4
════════════════════════════════════════════════════════
```
