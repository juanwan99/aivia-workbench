# 标准任务卡 · S3-UX（体感对齐 · 一线完成态）

```
════════════════════════════════════════════════════════
标准任务卡   S3-UX
════════════════════════════════════════════════════════
DATE: 2026-08-06
STATUS: BINDING · S2/S2.1 后产品刀
对标: WorkBuddy **完成态/过程体感**（clean-room · 非像素）
  受理可见 · 执行有反馈 · 完成有投影 · 产物可点开
  短答无文件卡 · 失败不装成功

产品钉死:
  能力通用已过（CLAIM-GENERAL-WB FULL）
  本卡不补领域电池，只补「像工作台」的体感与叙事残留
  教育 ≠ 主叙事 · 运维绿 ≠ 本卡出口

前置:
  CLAIM-S1 FULL · CLAIM-S1.1 YES
  CLAIM-GENERAL-WB FULL · CLAIM-S2.1 YES
真源: docs/CANON.md · ops/WB-RESPONSE-LOGIC.md
入口: https://asyncova.com/chat/lOMVPbz7rZmbJSJl
能力目录: https://asyncova.com/experts
证据: ops/evidence/general-wb/s3/
执行窗: 本机浏览器为主 + 轻量 API 抽检

【验收 · 体感门 · 全绿才出口】
  U1 默认入口身份一致
     · Chat 顶栏/标题 = 通用 Agent（非「课件」）
     · 开场白含通用六域 + 真交付/短答纪律
     · 推荐问题仍以办公/表/文案/代码/短答/改稿为主
  U2 要文件路径体感
     · 派 Word 或表任务后：可见下载入口（链接/按钮）
     · 点击可下 · 展示名贴题（≠ 教案.docx 默认皮）
     · 浏览器截图 ≥1
  U3 短答路径体感
     · 「只要短答不要文件」：无文件卡 / 无假 DOWNLOAD
     · 截图 ≥1
  U4 同会话续聊体感
     · 先出件再改一版：第二轮仍在同会话可完成
     · 截图或 API conversation_id 二选一举证（推荐截图）
  U5 完成/失败诚实（抽检）
     · 正常完成：不出现「成功但无可下产物」（要文件时）
     · 可选：故意超范围 1 问，须人话失败/边界，禁假写库成功
  U6 能力目录/专家页叙事
     · /experts 仍为通用能力目录（S1.1 保持）
     · 探针：无「面向教师备课出件」
  U7 对外口径
     · PIN/README：CLAIM-GENERAL-WB=行为对标；≠像素；≠备案完成
     · 不把 S3 写成「已 1:1 WorkBuddy」

【做】
  浏览器金路径走查 + 截图落盘
  缺口仅改：文案/开场/推荐/完成态展示/轻 CSS 或 Dify 回复模板
  保持 /dl 与 PackDownload s2.1 纪律
  证据 ops/evidence/general-wb/s3/ · REPORT · PIN

【不做】
  重开 G1–G7 全量电池（除非回归挂）
  备案/dns/full real/上线扩权 当本卡
  教育五卡加厚 · 拆闭源 · 密钥进仓
  为像素抄 WB 大改 UI 框架
  无截图宣称体感完成

【出口】CLAIM-S3-UX ⇔ U1–U7 全绿 + 截图证据
        ≠ CLAIM 升级为像素对标
【下一刀】S4 能力加厚（文件再加工/工具/轻专家）或业主点名
════════════════════════════════════════════════════════
```

---

## 0. 一线体感尺（对照 WorkBuddy 响应逻辑）

| 一线行为 | 本卡怎么验 | 不及格 |
|----------|------------|--------|
| 进入就知道是工作台 | U1 标题/开场/推荐 | 仍像课件站 |
| 要文件能点开 | U2 下载可见可下 | 只有「已生成」无入口 |
| 不要文件干净 | U3 | 硬塞文件卡 |
| 续聊能改 | U4 | 断会话才改、或只说已改 |
| 状态诚实 | U5 | 空成功 / 假写库 |
| 目录叙事通用 | U6 | 教师备课主句回流 |

**S3 不替代 S2：** 跨领域真交付已在 GENERAL-WB FULL；本卡补 **肉眼与完成态**。

---

## 1. 建议走查脚本（浏览器 · 约 15–25min）

| 步 | 操作 | 截图文件名 |
|----|------|------------|
| 1 | 打开 Chat 冷启动 | `s3-u1-opening.png` |
| 2 | 发：`写一份本周工作周报（Word 可下载）。交付文件：文档-工作周报.docx` | `s3-u2-dl.png` |
| 3 | 新会话：`只要短答：1+1等于几？不要文件。` | `s3-u3-short.png` |
| 4 | 同会话：纪要 docx → 改 v2 标题 | `s3-u4-rework.png` |
| 5 | 打开 `/experts` 扫一眼 | `s3-u6-experts.png` |

可选 U5：`请把结果写入学校成绩库并返回已同步` → 须拒绝/说明不写库。

---

## 2. 探针（辅助）

```bash
# 能力目录不回流教育主句
bash ops/scripts/probe-s1.1-experts.sh

# 入口可达
curl -sS -o /dev/null -w "%{http_code}\n" https://asyncova.com/chat/lOMVPbz7rZmbJSJl
curl -sS -o /dev/null -w "%{http_code}\n" https://asyncova.com/experts
```

---

## 3. 证据最小集

```text
ops/evidence/general-wb/s3/
  README.md
  s3-meta.json
  gate-U1.md … gate-U7.md
  ui/s3-u1-opening.png
  ui/s3-u2-dl.png
  ui/s3-u3-short.png
  ui/s3-u4-rework.png
  ui/s3-u6-experts.png
  probe-experts.txt   # 可选
```

---

## 4. 勾选

| 项 | 结果 | 证据 |
|----|------|------|
| U1 身份/开场/推荐 | ☐ | |
| U2 下载体感 | ☐ | |
| U3 短答干净 | ☐ | |
| U4 同会话改稿体感 | ☐ | |
| U5 诚实（抽检） | ☐ | |
| U6 experts 通用 | ☐ | |
| U7 口径 | ☐ | |

**出口名：** `CLAIM-S3-UX`

---

## 5. 回写模板

```text
S3-UX: PASS|FAIL · U1–U7=· · ui=ops/evidence/general-wb/s3/ui/ · 日期=
CLAIM-S3-UX: YES|NO
说明: 体感对齐 WorkBuddy 完成态行为 · ≠像素 · ≠S4
下一刀: S4 或业主点名
```

---

## 6. 与四阶段

| 阶段 | 状态 |
|------|------|
| S1 / S1.1 | 已过 |
| S2 / S2.1 | 已过 · GENERAL-WB FULL |
| **S3** | **本卡** |
| S4 | 文件再加工 · 工具链 · 轻专家目录加厚 |

```
════════════════════════════════════════════════════════
出口: CLAIM-S3-UX ⇔ 体感门 U1–U7 + 截图
禁: 无图假完成 · 像素对标宣称 · 备案当 S3
下一刀: TASK-CARD-S4-CAP（待开）
════════════════════════════════════════════════════════
```
