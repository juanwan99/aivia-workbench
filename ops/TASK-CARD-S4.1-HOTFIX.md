# 标准任务卡 · S4.1-HOTFIX（C2 再加工真修 · 电池加固 · 部署）

```
════════════════════════════════════════════════════════
标准任务卡   S4.1-HOTFIX
════════════════════════════════════════════════════════
DATE: 2026-08-06
STATUS: BINDING · 现行唯一产品刀
代号: S4 审查债收口
父卡: ops/TASK-CARD-S4-CAP.md
真源: docs/CANON.md

【审查结论（不可辩）】
  CLAIM-S4-CAP FULL = NO（审查）
  P0  C2 v2 xlsx = 交付清单套娃 · 非竞品数据再加工
  P0  幽灵 /dl 404（2f9d3c8e…）写进产物
  P0  电池只验 new_id/ooxml · 未验「市占率/产品C」→ 假绿
  P1  缺 ui/s4-c2-rework.png · 展示名退化「报表.xlsx」
  可保留绿: C1 / C3 / C4 / C5 / C6（勿无故重开全量）

【目标】
  同会话表格再加工 = 一线：旧表 → 真数据 v2 可下可开
  电池语义断言 + 浏览器 C2 帧 + 部署 PackDownload/提示词防套娃
  出口: CLAIM-S4.1-HOTFIX=YES → CLAIM-S4-CAP 升 FULL YES

前置: CLAIM-GENERAL-WB FULL · S3-UX YES · S4 部分证据已在仓
入口: https://asyncova.com/chat/lOMVPbz7rZmbJSJl
证据: ops/evidence/general-wb/s4.1/
  （可同时回写 s4/ 中 C2 产物与 results）
执行窗: API 重跑 C2 + 浏览器截图 + 按需 SSH/Dify 部署

════════════════════════════════════════════════════════
```

---

## 0. 一线尺（C2 专用）

| 一线行为 | PASS | FAIL（本次已中） |
|----------|------|------------------|
| 再加工改的是**数据** | sheet 含产品/单价/销量/市占率等 | sheet 只有「文件名/类型/下载」 |
| v2 完整新文件 | 新 `/dl` · 200 · OOXML | 只说已改；或套娃链 |
| 链接诚实 | 清单内每个 `/dl` 均 200 | 404 幽灵 id |
| 展示名贴题 | `表格-竞品-v2.xlsx` 类 | 默认 `报表.xlsx` |
| 同会话 | conversation_id 连续 | 断会话冒充 |

**铁律：** 有文件但内容是交付清单 = **FAIL**（不是 empty_success，是 **wrong_artifact**）。  
**铁律：** 电池不得仅靠 `ooxml==true` 判 C2 PASS。

---

## 1. 验收门（全绿才出口）

### F1 · PackDownload / 工作流防套娃（部署）

| 要求 | PASS |
|------|------|
| xlsx 打包输入必须是 **csv/数据表**，不得把「交付清单」markdown 表打成唯一 sheet | 单测或回归：输入含 `\| # \| 文件名 \|` 时拒绝或剥离开 |
| 多产物逻辑保留 s4 multi（C1 不回退） | C1 抽检仍双 `/dl` 或说明未改坏 |
| 默认名保持 文档/页面 · 禁教案皮 | 回归名 ≠ 教案.docx |
| 产物 | `deploy/packdownload/packdownload_s4.1.py`（或 s4 原地修订）已部署到现网节点 |

### F2 · 系统提示加厚（部署）

在 general-wb-s4 提示词中明确：

1. 再加工 = 输出 **完整新 csv 数据** + `交付文件：表格-…-v2.xlsx`  
2. **禁止** 在 csv 里写下载链接/文件名/类型列冒充业务表  
3. 用户要市占率/新行必须出现在 **数据区**  
4. 每个交付链接必须是本轮真实上传结果，禁止编造 `/dl/{id}`

产物：`ops/evidence/general-wb/s4.1/general-wb-s4.1-system.txt` 并发布。

### F3 · C2 重跑（硬门 · API + 本机打开）

**测句（同 conversation，一字不差）：**

| 轮 | 输入 |
|----|------|
| R1 | `做一张竞品表 Excel：产品A 单价99 月销120；产品B 单价79 月销200。列含产品、单价、月销量、估算月营收。交付文件：表格-竞品-v1.xlsx` |
| R2 | `基于上一版表格做再加工（完整新文件，不要只说 diff）：① 增加「市占率假设%」列（A=40，B=60）；② 增加一行产品C 单价89 月销150 市占率20；③ 营收列按单价×月销重算；④ 交付文件：表格-竞品-v2.xlsx` |

| 检查 | PASS |
|------|------|
| same conversation | R1/R2 同 `conversation_id` |
| 新 dl | R2 id ≠ R1 id |
| R2 公网 200 | curl/API |
| sheet 语义 | 含 **市占率**（或同义列）· **产品C/C** · A/B 仍在 · 营收合理（A11880/B15800/C13350） |
| **非套娃** | sheet **不得** 以「文件名/类型/下载」为业务列主表 |
| 全链接 200 | answer 内每个 `/dl` 均 200 · **零 404** |
| 展示名 | CD 或清单含 `竞品` 与 `v2`（或 `表格-竞品-v2.xlsx`）· **≠ 仅「报表.xlsx」** |
| 本机打开 | 人眼或脚本打印 cells 入证 |

证据：`artifacts/c2-v1.xlsx` · `c2-v2.xlsx` · `c2-r1/r2.answer.txt` · `gate-F3.md`

### F4 · 电池语义加固（防再假绿）

更新 `_battery`（s4.1 副本或补丁）：

```text
C2 PASS ⇔
  new_dl_id
  AND ooxml
  AND public_status==200 for ALL links in R2 answer
  AND sheet_text has 市占率|份额
  AND sheet_text has 产品C|产品 C|\bC\b with 89|150|20 near
  AND NOT (sheet has 文件名 AND 类型 AND 下载 AND lacks 单价)
  AND display_name not in (报表.xlsx,) unless also has 竞品-v2 alias
```

跑通：`python3 ops/evidence/general-wb/s4.1/_battery_c2.py` → C2 pass true 仅当上述成立。  
单元：放一份「套娃清单 xlsx」必须 **fail**。

### F5 · 浏览器轨补帧

| 文件 | 内容 |
|------|------|
| `ui/s4-c2-rework.png` | 同会话 R2 后交付清单 + 可点下载（展示名可见） |

可选：R1 一帧 `s4-c2-r1.png`。  
**无 F5 = 不得 FULL CLAIM**（继承双轨铁律）。

### F6 · 回归抽检（不重开全 S4）

| 抽检 | PASS |
|------|------|
| C1 或说明 multi 未回退 | 一次双文件仍可 · 或引用 s4 未改路径的 C1 证+一句「节点兼容」 |
| C5 拒 OA 仍绿 | 一句重跑或引用 s4 文本仍有效（提示词未放松写库） |
| empty_success=0 | 本卡电池 |

### F7 · 回写与远端可见

| 项 | PASS |
|----|------|
| `ops/evidence/general-wb/s4.1/` 齐全 | README · meta · results · gates · ui · artifacts |
| `ops/S4.1-HOTFIX-REPORT.md` | 写清根因=套娃打包 / 电池洞 |
| PIN | `CLAIM-S4.1-HOTFIX=YES` · `CLAIM-S4-CAP=FULL YES` |
| TASK-CARD-NOW | 维护态或业主下一刀 |
| **git push** · main 可 list | D6 级铁律 |

---

## 2. 部署顺序

```text
1) git pull · 读本卡
2) 修 packdownload_s4.1.py（拒套娃 sheet / 优先 csv 数据区）
3) 修系统提示 s4.1 · 发布 workflow/App
4) 单元：套娃样本必须 FAIL；真 csv → xlsx OK
5) API 重跑 C2 两轮 · 本机 print cells
6) 电池 F4 断言全过
7) 浏览器截 s4-c2-rework.png
8) F6 轻回归
9) 写 REPORT + PIN · push
10) 仅此时 CLAIM-S4-CAP FULL
```

---

## 3. 证据最小集

```text
ops/evidence/general-wb/s4.1/
  README.md
  s4.1-meta.json
  results.json
  gate-F1.md … gate-F7.md
  packdownload_s4.1.py
  general-wb-s4.1-system.txt
  _battery_c2.py
  _unit_nested_sheet_fail.py   # 套娃必须红
  artifacts/c2-v1.xlsx
  artifacts/c2-v2.xlsx
  artifacts/c2-r1.answer.txt
  artifacts/c2-r2.answer.txt
  artifacts/c2-v2.cells.txt    # 打印出的单元格
  ui/s4-c2-rework.png
ops/S4.1-HOTFIX-REPORT.md
deploy/packdownload/packdownload_s4.1.py
```

---

## 4. 勾选

| 项 | 结果 | 证据 |
|----|------|------|
| F1 部署防套娃 | ☐ | |
| F2 提示词发布 | ☐ | |
| F3 C2 数据 v2 真绿 | ☐ | |
| F4 电池语义 + 套娃单测红 | ☐ | |
| F5 c2 截图 | ☐ | |
| F6 轻回归 | ☐ | |
| F7 push + PIN FULL | ☐ | |

**出口名：** `CLAIM-S4.1-HOTFIX` → 拉动 `CLAIM-S4-CAP=FULL YES`  
**PASS：** F1–F7 全 PASS。

---

## 5. 不做

- 无 F3 数据验就改 PIN 假 FULL  
- 用 s4 旧坏 v2 充数  
- 备案/教育主线/像素抄/密钥进仓  
- 为过线删掉 C2 门禁  
- 重跑 C1–C6 全量除非 F1 可能打坏 multi  

---

## 6. 回写模板

```text
S4.1-HOTFIX: PASS|FAIL · F1–F7=· · C2 cells=市占率+产品C · 404链接=0 · 日期=
CLAIM-S4.1-HOTFIX: YES
CLAIM-S4-CAP: FULL YES
说明: 再加工真数据 · 电池语义加固 · ≠像素
下一刀: 维护态 / 业主点名
```

---

## 7. 交接点名

> 审查已证明：S4 差在 **再加工真伪**，不差在「会不会出两个文件」。  
> 本卡只收 C2 + 防再假绿；收完才允许 CLAIM-S4-CAP FULL。

```
════════════════════════════════════════════════════════
出口: CLAIM-S4.1-HOTFIX ⇔ F1–F7
      → CLAIM-S4-CAP FULL YES
禁: 套娃表假绿 · 404 链接 · 无截图 · 无 push
下一刀: 维护态
════════════════════════════════════════════════════════
```
