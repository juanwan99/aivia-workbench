# 标准任务卡 · S2.1-HOTFIX（审查债 · 修复部署）

```
════════════════════════════════════════════════════════
标准任务卡   S2.1-HOTFIX
════════════════════════════════════════════════════════
DATE: 2026-08-06
STATUS: BINDING · S2 条件绿后热修
前置: CLAIM-GENERAL-WB = CONDITIONAL YES（审查）
真源: docs/CANON.md
证据: ops/evidence/general-wb/s2.1/
对标: 一线观感 — 无教育默认文件名 · 分析有结论 · 代码默认可跑

【背景 · 审查 P1/P2】
  P1-1 G7 缺「3 条中性观察」（表有、文无）
  P1-2 PackDownload 默认文件名「教案.docx/课件.html」教育皮
  P2   G6 空 stdin 非 TTY 失败（isatty 脚枪）

【验收 · 全绿才出口】
  F1 PackDownload 默认名去教育皮（部署代码节点）
     · docx 默认 文档.docx · html 页面.html · md 文档.md
     · 仓内产物: deploy/packdownload/packdownload_s2.1.py
     · 回归: 纪要任务展示名 ≠ 教案.docx
  F2 系统提示 S2.1 已发布（分析必 3 观察 · 交付文件贴题命名）
     · ops/evidence/general-wb/s2.1/general-wb-s2.1-system.txt
  F3 G7 重跑 PASS
     · 测句同 S2 卡 G7
     · answer 含 ≥3 条中性观察（编号）
     · 无荐股/稳赚 · xlsx /dl 仍绿
     · python3 _assert_g7_obs.py g7.answer.txt → exit 0
  F4 G4 抽检文件名
     · 纪要/v2 下载展示名含 文档/纪要 等，不得为「教案.docx」
  F5 G6 空 stdin 可跑（参考脚本或模型输出等价逻辑）
     · g6-script-fixed.py </dev/null → exit 0
  F6 证据落盘 + PIN 回写
     · ops/evidence/general-wb/s2.1/
     · CLAIM-S2.1-HOTFIX=YES → CLAIM-GENERAL-WB 升 FULL YES

【做】
  1) 源站 Dify：PackDownload 代码节点替换为 packdownload_s2.1.py
  2) 发布 general-wb-s2.1-system.txt 到默认 App 系统提示
  3) 重跑 G7（必）· G4 一轮抽检（必）· G6 脚本自测（必）
  4) 浏览器可选 1 张 G7 截图
  5) 写 gate-F* · results · REPORT · PIN

【不做】
  备案/dns/full real · 教育加厚 · 拆闭源 · 密钥进仓
  重开 S2 全电池除非 F3/F4 失败
  宣称像素 1:1 WorkBuddy

【出口】CLAIM-S2.1-HOTFIX ⇔ F1–F6 全绿
        → CLAIM-GENERAL-WB = FULL YES（字面债关闭）
【下一刀】S3 体感对齐 或 业主点名
════════════════════════════════════════════════════════
```

---

## 部署步骤（源站）

```bash
cd /path/to/aivia-workbench && git pull

# 1) PackDownload：在 Dify 工作流 general-wb-s1 的 PackDownload 代码节点
#    粘贴 deploy/packdownload/packdownload_s2.1.py 全文并保存发布
#    （或沿用你们既有 _publish / 节点更新脚本，禁止打印密钥）

# 2) 系统提示：用 s2.1/general-wb-s2.1-system.txt 覆盖 App 系统提示并发布

# 3) 回归
# G7 测句见父卡 S2；保存 answer →
python3 ops/evidence/general-wb/s2.1/_assert_g7_obs.py /path/to/g7.answer.txt
# G4 一眼：展示文件名
# G6:
python3 ops/evidence/general-wb/s2.1/g6-script-fixed.py </dev/null
```

## 强制测句（F3）

```
请根据下列假设数据做竞品对比，输出 Excel 可下载：产品A 单价99元 月销量120；产品B 单价79元 月销量200。表至少含：产品、单价、月销量、估算月营收。再在正文给出 3 条中性观察（编号1.2.3.）。不要投资建议、不要荐股、不要「稳赚」话术。交付文件：表格-竞品对比.xlsx
```

## 强制测句（F4 文件名）

```
请生成《项目启动会纪要》Word 可下载。交付文件：文档-项目启动会纪要.docx
```
期望：下载清单文件名 **不是** 教案.docx。

## 回写

```text
S2.1-HOTFIX: PASS|FAIL · F1–F6=· · 日期=
CLAIM-GENERAL-WB: FULL YES
≠ 像素 · ≠ S3/S4 · ≠ 备案
下一刀: S3
```
