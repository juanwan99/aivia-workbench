# DOC-SOLID 短报告

```
DATE: 2026-08-06
入口: https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl
DOC-SOLID: PASS
CLAIM-DOC-SOLID: YES
正式上线: 否
full real: 否（fixture）
空成功: 0
S2: DOCX 满绿（非 MD 债）
```

## 1. 结论（一句话）

现网 Chatflow 已支持 **真 XLSX 报表** 与 **真 DOCX 教案** 一键下载；本机 Excel/Word COM 打开通过；金路径回归空成功 **0**；可报 **CLAIM-DOC-SOLID**。**≠** 正式上线，**≠** WorkBuddy 全量复制，**≠** full real。

## 2. 云端改动

| 项 | 内容 |
|----|------|
| 应用 | Aivia 课件 · advanced-chat · site `lOMVPbz7rZmbJSJl` |
| 工作流 | 发布 `doc-solid` 版本（PackDownload 支持 xlsx/docx/html/md） |
| Code | 纯 stdlib OOXML 打包 → data-URL（sandbox 无 openpyxl） |
| LLM | 系统提示扩展：Excel CSV→xlsx、教案 MD→docx、拒写库 |
| 推荐问题 | +「要 Excel 表」「Word 教案」 |
| 数据 MODE | fixture（合成表） |

## 3. 段结果

| 段 | 结果 | 证据 |
|----|------|------|
| S0 冷启动 | PASS | parameters 有壳；suggested 含表/文档 |
| S1 XLSX | PASS | `s1-artifact.xlsx` · 改稿 `s1-rev-artifact.xlsx` |
| S1 本地开 | PASS | Excel COM rows=6 · openpyxl 表头+≥3 行 |
| S2 DOCX | PASS | `s2-artifact.docx` · 改稿 `s2-rev-artifact.docx` |
| S2 本地开 | PASS | Word COM text_len≈1530 |
| S3 R-G1 HTML | PASS | `r-g1-artifact.html` |
| S3 R-G3 大纲 | PASS | 无 DOWNLOAD_READY |
| S3 R-G4 拒写库 | PASS | 人话拒绝 · quote-aware |
| S3 R-X XLSX | PASS | `r-x-artifact.xlsx` |
| S4 体感 | PASS | 推荐问题含 Excel/Word |
| 空成功 | **0** | meta |

## 4. 本地测协议

1. 公网 Chat / Web API（同 app · X-App-Code + passport）发送真人话  
2. 解析 DOWNLOAD_READY data-URL → 落盘  
3. **Windows Excel COM + Word COM** 打开  
4. 产物进 `ops/evidence/doc-solid/`  

API 烟测辅助；**以本地打开为准**。

## 5. CLAIM

```text
CLAIM-DOC-SOLID: YES
正式上线: 否
full real: 否
DOCX: 满绿
```

## 6. 风险 / 下一刀

| 风险 | 说明 |
|------|------|
| data-URL 体积 | 大表可能超消息长度；报表宜控制行数或改文件存储 |
| DOCX 样式 | 现为最小 OOXML（段落/标题），非精美模板 |
| 模型波动 | 空成功门禁；回归可再跑 R-X / G1 |

**下一刀（择一，非本包）：** 文件节点/短链替代超大 data-URL · edu live 只读 · 全校上线授权（需业主）

## 7. 禁止复读

- 假全校上线 / 假 full real / 假 WorkBuddy 全量  
- 空成功 / 口头完毕  
- Agent 写库 · 密钥进仓 · Harness 主线  
