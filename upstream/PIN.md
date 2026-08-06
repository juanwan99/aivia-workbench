# 上游版本钉扎

```
STATUS: P0-GATE=PASS · CLAIM-B=YES · CLAIM-DOC-SOLID=YES · DL-FIX=PASS · CLAIM-SCENE-FULL=YES · WB-SURVEY=DONE · CLAIM-WB-SURVEY=YES · E1=PASS(LE) · hybrid · 正式上线=否
DATE: 2026-08-06
ONE_LINE: CLAIM-WB-SURVEY=YES（本机深查 UI/逻辑/组织 · 矩阵48/G17）；≠功能对齐 · ≠上线
```

| 组件 | 版本 | 日期 | 备注 |
|------|------|------|------|
| **Dify** | `1.16.1` | 2026-08-05 | Chat `lOMVPbz7rZmbJSJl` |
| DeepSeek | `deepseek-chat` | 2026-08-05 | 默认 LLM |
| **TLS** | **Let's Encrypt YE2** | 2026-08-06 | DNS-01 acme.sh |
| **bridge** | **0.2.1 hybrid** | 2026-08-06 | `/dl` 落盘 |
| **DOC-SOLID** | **PASS** | 2026-08-06 | 真 xlsx + 真 docx |
| **DL-FIX** | **PASS** | 2026-08-06 | **主路径=https 文件 URL** |
| **SCENE-FULL** | **PASS** | 2026-08-06 | **CLAIM-SCENE-FULL=YES** |
| **WB-SURVEY** | **DONE** | 2026-08-06 | **本机深查** · MATRIX 48/G17 |
| WorkBuddy 对照本机 | **5.3.5** | 2026-08-06 | 仅调查参照 · 非依赖 |
| OpenWork | 二期 | | 非主线 |

> 密钥 / IP / SSH **不进本文件**。  
> **下载主路径：** `https://workbench.aivia.asia/dl/{id}/file.{ext}`

## WB-SURVEY 出口

| 项 | 结果 |
|----|------|
| **WB-SURVEY** | **DONE** |
| **CLAIM-WB-SURVEY** | **YES** |
| 深查 | UI + 响应逻辑 + 组织 + 矩阵 |
| 矩阵 | `ops/WB-FEATURE-MATRIX.md` · **48** · **G=17** |
| IA/逻辑/组织 | `WB-IA.md` · `WB-RESPONSE-LOGIC.md` · `WB-ORG-MODEL.md` |
| 证据 | `ops/evidence/wb-survey/` |
| 开发实现 | **否** |
| 正式上线 | **否** |

## SCENE-FULL / 其它已收

| 项 | 结果 |
|----|------|
| CLAIM-B | YES |
| CLAIM-DOC-SOLID | YES |
| DL-FIX | PASS · https /dl |
| CLAIM-SCENE-FULL | YES |
| E1 | PASS（LE YE2） |
| CLAIM-C-REAL full | NO（hybrid） |
