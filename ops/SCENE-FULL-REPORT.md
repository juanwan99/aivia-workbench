# SCENE-FULL 短报告

```
DATE: 2026-08-06
入口: https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl
PHASE-SCENE-FULL: PASS
CLAIM-SCENE-FULL: YES
主路径: https://workbench.aivia.asia/dl/...
data-URL 主路径: 否
空成功: 0
正式上线: 否
```

## 1. 结论

个人 P0 场景矩阵 **S1–S8 全 PASS**：课件 HTML、教案 DOCX、Excel 表、大纲无假绿、同会话改稿、拒写库、连续三任务不串台、`/dl` 浏览器可下。  
**CLAIM-SCENE-FULL=YES**。≠ 全校上线 · ≠ WorkBuddy 1:1 · ≠ 模型重训。

## 2. 云端

| 项 | 内容 |
|----|------|
| 工作流 | `scene-full` 发布：多场景意图/防串台系统提示 |
| 推荐问题 | 课件 / Word / Excel / 大纲 |
| 出件 | PackDownload → bridge `/dl`（沿用 DL-FIX） |

## 3. 矩阵

| ID | 结果 | 证据要点 |
|----|------|----------|
| S1 HTML | PASS · 2 学科 | `s1a` 生物 · `s1b` 数学 |
| S2 DOCX | PASS · ≥2 说法 | `s2b/c/d` 真 OOXML；s2a 偶发 md 见债 |
| S3 XLSX | PASS · 2 说法 | 表头+≥3 行 · 本机 Excel 打开 |
| S4 大纲 | PASS | 无 DOWNLOAD_READY |
| S5 改稿 | PASS | DOCX+XLSX 同会话新 `/dl` |
| S6 拒写库 | PASS · 2 说法 | 人话拒绝 |
| S7 连续 | PASS | 课件→表→大纲，类型正确 |
| S8 点下 | PASS | Chrome UA · attachment · 无 blocked |

空成功：**0** · data-URL 主路径：**0**

## 4. 本地测

- 公网 `/dl` GET 200 + attachment  
- 本机 openpyxl / Excel COM 打开 XLSX  
- 真 DOCX zip+文本长度校验  
- HTML 可开  

## 5. P1

跳过手机下载 / 大表上限（见 `debts.md`）。

## 6. CLAIM

```text
CLAIM-SCENE-FULL: YES
正式上线: 否
主路径: https /dl
```
