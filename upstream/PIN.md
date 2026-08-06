# 上游版本钉扎

```
STATUS: CLAIM-WB-ALIGN=YES · CLAIM-WB-SURVEY=YES · CLAIM-SCENE-FULL=YES · CLAIM-B=YES · DOC-SOLID · DL-FIX · bridge=0.2.2 · 正式上线=否
DATE: 2026-08-06
ONE_LINE: CLAIM-WB-ALIGN=YES（P0+P1 可验收 · 非1:1 · 非自动上线）；主路径仍 https /dl
```

| 组件 | 版本 | 日期 | 备注 |
|------|------|------|------|
| **Dify** | `1.16.1` | 2026-08-05 | Chat `lOMVPbz7rZmbJSJl` |
| DeepSeek | `deepseek-chat` | 2026-08-05 | 默认 LLM |
| **TLS** | **Let's Encrypt YE2** | 2026-08-06 | DNS-01 acme.sh |
| **bridge** | **0.2.2 hybrid** | 2026-08-06 | `/dl` + **ops metrics** |
| **DOC-SOLID** | **PASS** | 2026-08-06 | 真 xlsx + 真 docx |
| **DL-FIX** | **PASS** | 2026-08-06 | **主路径=https 文件 URL** |
| **SCENE-FULL** | **PASS** | 2026-08-06 | CLAIM-SCENE-FULL=YES |
| **WB-SURVEY** | **DONE** | 2026-08-06 | 本机 live · 48/G17 |
| **WB-ALIGN** | **PASS** | 2026-08-06 | **CLAIM-WB-ALIGN=YES** |
| OpenWork | 二期 | | 非主线 |

> 密钥 / IP / SSH **不进本文件**。  
> **下载主路径：** `https://workbench.aivia.asia/dl/{id}/file.{ext}`

## WB-ALIGN 出口

| 项 | 结果 |
|----|------|
| **CLAIM-WB-ALIGN** | **YES** |
| S0–S5 + FINAL | **PASS** |
| 空成功 | **0** |
| 证据 | `ops/evidence/wb-align/` |
| 矩阵状态 | `ops/WB-ALIGN-MATRIX-STATUS.md` |
| 正式上线 | **否** |
| 1:1 复制 | **否** |
