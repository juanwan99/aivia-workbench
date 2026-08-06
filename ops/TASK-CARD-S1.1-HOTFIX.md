# 标准任务卡 · S1.1-HOTFIX（审查后完善 · 修复 · 部署）

```
════════════════════════════════════════════════════════
标准任务卡   S1.1-HOTFIX
════════════════════════════════════════════════════════
DATE: 2026-08-06
STATUS: BINDING · S1 条件绿后的热修刀
前置: CLAIM-S1-GENERAL-WB = CONDITIONAL YES（审查 2026-08-06）
真源: docs/CANON.md > HANDOFF > 本卡
父卡: ops/TASK-CARD-S1-GENERAL-WB.md
证据: ops/evidence/general-wb/s1.1/
产物: deploy/aivia-experts/index.html

【背景】
  S1 G1–G3 /dl 与通用系统提示已绿；审查指出：
  P1-1 /experts 仍「面向教师备课」教育主叙事
  P1-2 缺浏览器体感截图
  P1-3 PIN/入口表述：根域 ≠ Chat 工作台
  P2   G2 无合计行（可选顺手）

【目标】
  关闭 S1 条件项 → CLAIM-S1 升为 FULL YES（仍 ≠ CLAIM-GENERAL-WB）
  不碰备案/dns/full real；不开教育加厚主线

执行窗: SSH 源站/边缘静态目录 + 本机浏览器截图
  静态页路径（现网）: /var/www/aivia-experts/index.html
  公网: https://asyncova.com/experts 与 /experts/
════════════════════════════════════════════════════════
```

---

## 1. 做 / 不做

### 做

| ID | 项 | 过线 |
|----|----|------|
| H1 | 部署通用化 `/experts` 页 | 页标题/导语无「面向教师备课」主句；卡片以办公/表/文案/代码/短答/改稿为主；教育最多 1 张且标「可选领域」 |
| H2 | 同步 catalog.yaml v2 | 与页面卡片一致；落盘 evidence |
| H3 | 浏览器体感截图 ≥4 | Chat 开场+推荐 · G1 下载可见 · G3 无文件卡 · experts 新文案 |
| H4 | PIN / README 入口一句 | 写明 Chat 全路径；根域=公司站 |
| H5 | 公网探针 | `/experts` `/experts/` 200；正文含「通用」；**不含**「面向教师备课出件」 |
| H6 | （可选）G2 合计行 | 系统提示 XLSX 条加「可含合计行」；不挡 H1–H5 |

### 不做

- 备案 / dns_ali / full real  
- 教育五卡加厚、QUAD 当对标  
- 改 PackDownload token / 拆 bridge（无必要）  
- 宣称 CLAIM-GENERAL-WB 或 WorkBuddy 全量对标完成  
- 密钥进仓  

---

## 2. 部署步骤（源站）

```bash
# 1) 取热修产物（本仓）
#    deploy/aivia-experts/index.html
#    或 ops/evidence/general-wb/s1.1/experts/index.html

# 2) 备份并发布
sudo mkdir -p /var/www/aivia-experts
sudo cp -a /var/www/aivia-experts/index.html /var/www/aivia-experts/index.html.bak.$(date +%Y%m%d%H%M) 2>/dev/null || true
sudo cp deploy/aivia-experts/index.html /var/www/aivia-experts/index.html
sudo chmod 644 /var/www/aivia-experts/index.html

# 3) nginx 已有 location（见 ops/evidence/quad-fix-deploy/edge/workbench-experts.nginx.conf）
#    确认 /experts 与 /experts/ 均 alias 到该目录，禁止 302 到 :8443
sudo nginx -t && sudo systemctl reload nginx   # 或边缘等价

# 4) 若边缘反代缓存：purge /experts 或短 Cache-Control 已是 no-cache
```

边缘 asyncova：若专家页在源站经隧道透传，**只改源站静态文件**即可；若边缘有独立拷贝，两边同步。

---

## 3. 验收探针

```bash
# 文案
curl -sS https://asyncova.com/experts | tee /tmp/ex.html | grep -E '通用|面向教师备课|课件专家|办公 Word'
# 期望：有「通用」与「办公 Word」；无「面向教师备课出件」

curl -sS -o /dev/null -w "%{http_code}\n" https://asyncova.com/experts
curl -sS -o /dev/null -w "%{http_code}\n" https://asyncova.com/experts/
# 期望：200 200

# 负向
! grep -q '面向教师备课出件' /tmp/ex.html
```

浏览器清单（截图进 `ops/evidence/general-wb/s1.1/ui/`）：

| 文件 | 内容 |
|------|------|
| `ui-chat-opening.png` | 开场白 + 推荐问题可见 |
| `ui-g1-dl.png` | Word 任务后下载链接/按钮 |
| `ui-g3-short.png` | 短答无文件卡 |
| `ui-experts.png` | 新能力目录全文案 |

---

## 4. 勾选

| 项 | 结果 | 证据 |
|----|------|------|
| H1 experts 部署 | ☐ | curl + ui-experts.png |
| H2 catalog v2 | ☐ | s1.1/experts/catalog.yaml |
| H3 截图≥4 | ☐ | s1.1/ui/* |
| H4 PIN 入口句 | ☐ | upstream/PIN.md |
| H5 探针 200+文案 | ☐ | s1.1/probe-experts.txt |
| H6 G2 合计（可选） | ☐ / skip | |

**出口名**：`CLAIM-S1.1-HOTFIX`  
**升格**：上述 H1–H5 PASS → 可把 S1 从 CONDITIONAL 记为 **FULL YES**（仍 ≠ CLAIM-GENERAL-WB）

---

## 5. 回写模板

```text
S1.1-HOTFIX: PASS|FAIL · H1–H5=· · experts=通用能力目录 · ui=ops/evidence/general-wb/s1.1/ui/ · 日期=
CLAIM-S1-GENERAL-WB: FULL YES（体感截图+experts 已清教育主句）
下一刀: S2-GENERAL-WB（G4–G7）
```

---

## 6. 交接点名

> S1.1 只补审查债：专家页去教育皮、浏览器看得见、入口说清楚。  
> 不拿运维绿冒充对标；全量对标仍看 S2 电池。

```
════════════════════════════════════════════════════════
出口: CLAIM-S1.1-HOTFIX ⇔ H1–H5 绿
下一刀: TASK-CARD-S2-GENERAL-WB
════════════════════════════════════════════════════════
```
