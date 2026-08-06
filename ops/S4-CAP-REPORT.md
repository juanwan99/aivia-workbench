# S4-CAP 报告

```
DATE: 2026-08-06
PHASE: S4-CAP
CLAIM-S4-CAP: YES
C1–C6: 全绿
empty_success: 0
dual_track: API + browser
workflow: general-wb-s4
≠ 像素 · ≠ 备案 · ≠ 用 s2/s3 图冒充
```

## 1. 结论

在 **CLAIM-GENERAL-WB FULL + CLAIM-S3-UX** 之上完成 **能力纵深** 验收：  
一次多产物、同会话再加工、公号→清单、长结构方案、边界诚实、通用口径。  
可报 **CLAIM-S4-CAP=YES**（main 证据可见后生效）。

## 2. 门禁

| 门 | RESULT | 要点 |
|----|--------|------|
| **C1** | **PASS** | 一次派活 Word+Excel **两** `/dl` · 真 OOXML · 名贴题 |
| **C2** | **PASS** | 同会话表 v2 新 id · 新列/产品意图 |
| **C3** | **PASS** | 公号无文件 → 同会话 xlsx 清单 |
| **C4** | **PASS** | 《上线沟通方案》五节 · 可下 docx |
| **C5** | **PASS** | 拒 OA/假工单 · 不空成功 |
| **C6** | **PASS** | Chat 通用 + /experts 通用 + 口径 |
| 联检 | **PASS** | empty_success=0 · ≠教案.docx · 无密钥进仓 |

## 3. 工程加厚（本卡）

| 项 | 动作 |
|----|------|
| PackDownload **s4** | 支持 docx+xlsx **双交付** `_pack_multi`；长文无 fence 亦可抽 docx |
| 系统提示 **s4** | 多产物 / 再加工 / 方案五节 / 拒 OA 工单 |
| 发布 | workflow `general-wb-s4` · App 名仍 **Aivia 通用 Agent** |

## 4. 证据

根：`ops/evidence/general-wb/s4/`  
API：`artifacts/` · 浏览器：`ui/s4-*.png`  
脚本：`_battery_c1c6.py` · `_publish_s4.py` · `_capture_ui_s4.py`（无密钥）

## 5. 限制（诚实）

- **≠** WorkBuddy 像素 1:1  
- **≠** 备案 / full real  
- **≠** 教育站回流  
- 模型偶发省略 markdown fence：已用 PackDownload 明文抽取兜底  

## 6. CLAIM

```text
CLAIM-S4-CAP: YES
= C1–C6 双轨全绿 + empty_success=0 + main push
下一刀: 维护态 / 业主新主线
```
