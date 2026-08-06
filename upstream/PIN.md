# 上游版本钉扎

```
STATUS: P0-GATE=PASS · CLAIM-B=YES · CLAIM-DOC-SOLID=YES · E1=PASS(LE) · hybrid · 正式上线=否
DATE: 2026-08-06
ONE_LINE: 文档/报表扎实（XLSX+DOCX）；CLAIM-B 仍 YES；非全校上线；full real 否
```

| 组件 | 版本 | 日期 | 备注 |
|------|------|------|------|
| **Dify** | `1.16.1` | 2026-08-05 | Chat `lOMVPbz7rZmbJSJl` |
| DeepSeek | `deepseek-chat` | 2026-08-05 | 默认 LLM |
| **TLS** | **Let's Encrypt YE2** | 2026-08-06 | DNS-01 acme.sh |
| **bridge** | **0.2.0 hybrid** | 2026-08-06 | host + aivia-bridge 容器 |
| **DOC-SOLID** | **PASS** | 2026-08-06 | 真 xlsx + 真 docx · 空成功 0 |
| OpenWork | 二期 | | 非主线 |

> 密钥 / IP / SSH **不进本文件**。

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
| 正式上线 | **否** |

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
