# 上游版本钉扎

```
STATUS: P0-GATE=PASS · CLAIM-B=YES · CLAIM-DOC-SOLID=YES · DL-FIX=PASS · E1=PASS(LE) · hybrid · 正式上线=否
DATE: 2026-08-06
ONE_LINE: 主路径=https 文件 URL；XLSX/DOCX/HTML 可真下；CLAIM-B 仍 YES；非全校上线
```

| 组件 | 版本 | 日期 | 备注 |
|------|------|------|------|
| **Dify** | `1.16.1` | 2026-08-05 | Chat `lOMVPbz7rZmbJSJl` |
| DeepSeek | `deepseek-chat` | 2026-08-05 | 默认 LLM |
| **TLS** | **Let's Encrypt YE2** | 2026-08-06 | DNS-01 acme.sh |
| **bridge** | **0.2.1 hybrid** | 2026-08-06 | + `/dl` 落盘；下载主路径 HTTPS |
| **DOC-SOLID** | **PASS** | 2026-08-06 | 真 xlsx + 真 docx · 空成功 0 |
| **DL-FIX** | **PASS** | 2026-08-06 | **主路径=https 文件 URL**（非 data-URL） |
| OpenWork | 二期 | | 非主线 |

> 密钥 / IP / SSH **不进本文件**。  
> **下载主路径：** `https://workbench.aivia.asia/dl/{id}/file.{ext}`

## P0-GATE 出口

| 项 | 结果 |
|----|------|
| 段 A 稳定 | **PASS** |
| 段 B 金路径 | **PASS** · 空成功 **0** |
| 证据 | `ops/evidence/p0-gate/` |
| **CLAIM-B** | **YES** |
| 正式上线 | **否** |
| full real | **跳过**（hybrid） |
| **P0-GATE** | **PASS** |

## DOC-SOLID 出口

| 项 | 结果 |
|----|------|
| **CLAIM-DOC-SOLID** | **YES** |
| S1 XLSX | PASS · 本地 Excel 打开 |
| S2 DOCX | PASS · 本地 Word 打开 |
| 空成功 | **0** |
| 证据 | `ops/evidence/doc-solid/` |

## DL-FIX 出口

| 项 | 结果 |
|----|------|
| **PHASE-DL-FIX** | **PASS** |
| 主路径 | **https 文件 URL** |
| data-URL 主路径 | **否** |
| HTML/XLSX/DOCX | 公网 attachment 下载 |
| 证据 | `ops/evidence/dl-fix/` |

## E1

| 项 | 结果 |
|----|------|
| **E1** | **PASS**（LE YE2） |

## C-REAL

| 项 | 结果 |
|----|------|
| **CLAIM-C-REAL(hybrid)** | **YES** |
| CLAIM-C-REAL full | **NO** |

## D-LITE

| 项 | 结果 |
|----|------|
| **CLAIM-D-LITE** | **YES** |
