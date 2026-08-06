# 上游版本钉扎

```
STATUS: P0-GATE=PASS · CLAIM-B=YES · CLAIM-DOC-SOLID=YES · DL-FIX=PASS · CLAIM-SCENE-FULL=YES · E1=PASS(LE) · hybrid · 正式上线=否
DATE: 2026-08-06
ONE_LINE: CLAIM-SCENE-FULL=YES；主路径=https 文件 URL；个人全场景 P0 矩阵绿；非全校上线
```

| 组件 | 版本 | 日期 | 备注 |
|------|------|------|------|
| **Dify** | `1.16.1` | 2026-08-05 | Chat `lOMVPbz7rZmbJSJl` |
| DeepSeek | `deepseek-chat` | 2026-08-05 | 默认 LLM |
| **TLS** | **Let's Encrypt YE2** | 2026-08-06 | DNS-01 acme.sh |
| **bridge** | **0.2.1 hybrid** | 2026-08-06 | `/dl` 落盘 |
| **DOC-SOLID** | **PASS** | 2026-08-06 | 真 xlsx + 真 docx |
| **DL-FIX** | **PASS** | 2026-08-06 | **主路径=https 文件 URL** |
| **SCENE-FULL** | **PASS** | 2026-08-06 | **CLAIM-SCENE-FULL=YES** · S1–S8 |
| OpenWork | 二期 | | 非主线 |

> 密钥 / IP / SSH **不进本文件**。  
> **下载主路径：** `https://workbench.aivia.asia/dl/{id}/file.{ext}`

## P0-GATE 出口

| 项 | 结果 |
|----|------|
| **CLAIM-B** | **YES** |
| 正式上线 | **否** |
| **P0-GATE** | **PASS** |

## DOC-SOLID 出口

| 项 | 结果 |
|----|------|
| **CLAIM-DOC-SOLID** | **YES** |

## DL-FIX 出口

| 项 | 结果 |
|----|------|
| **PHASE-DL-FIX** | **PASS** |
| 主路径 | **https 文件 URL** |

## SCENE-FULL 出口

| 项 | 结果 |
|----|------|
| **CLAIM-SCENE-FULL** | **YES** |
| S1–S8 | **PASS** |
| 空成功 | **0** |
| 主路径 | **https /dl** |
| 证据 | `ops/evidence/scene-full/` |
| 正式上线 | **否** |

## E1 / C-REAL / D-LITE

| 项 | 结果 |
|----|------|
| E1 | PASS（LE YE2） |
| CLAIM-C-REAL(hybrid) | YES |
| CLAIM-C-REAL full | NO |
| CLAIM-D-LITE | YES |
