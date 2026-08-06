# 标准任务卡 · S1.1-HOTFIX（审查债 · 完善修复部署）

```
════════════════════════════════════════════════════════
标准任务卡   S1.1-HOTFIX
════════════════════════════════════════════════════════
产品钉死（业主）:
  能力通用   什么都能干
  对标 WorkBuddy 行为 · 非教育垂直站
  S1 G1–G3 已绿；本卡只关审查 P1 债

前置: CLAIM-S1-GENERAL-WB = YES（条件绿）
执行窗: SSH 静态页 + 本机浏览器截图
真源: docs/CANON.md
证据: ops/evidence/general-wb/s1.1/
部署产物: deploy/aivia-experts/index.html
  → 现网 /var/www/aivia-experts/index.html
公网: https://asyncova.com/experts
Chat: https://asyncova.com/chat/lOMVPbz7rZmbJSJl

【验收 · 五项 · 全绿才出口】
  H1 /experts 通用化部署
     · 无「面向教师备课出件」
     · 有「通用」+ 办公 Word/Excel/公号/代码/短答/改稿
     · 教育最多 1 张且标「可选领域」
  H2 catalog.yaml v2 与页面一致（ops/experts/）
  H3 浏览器截图 ≥4
     · ui-chat-opening · ui-g1-dl · ui-g3-short · ui-experts
     · 目录 ops/evidence/general-wb/s1.1/ui/
  H4 PIN/入口句：根域≠工作台；Chat 写全路径
  H5 探针 PASS
     · bash ops/scripts/probe-s1.1-experts.sh
     · /experts 与 /experts/ 均 200

【做】
  git pull
  sudo cp deploy/aivia-experts/index.html /var/www/aivia-experts/index.html
  nginx reload（按现网）
  探针 + 截图 + 回写 PIN
  边缘若有静态副本则同步

【不做】
  备案/dns/full real 当本卡
  教育五卡加厚 · QUAD=对标
  改 bridge token · 拆闭源 · 密钥进仓
  宣称 CLAIM-GENERAL-WB（那是 S2）

【出口】CLAIM-S1.1-HOTFIX ⇔ H1–H5 全绿
        → CLAIM-S1 升 FULL YES（仍 ≠ 全量对标）
【下一刀】TASK-CARD-S2-GENERAL-WB（G4–G7）
════════════════════════════════════════════════════════
```
