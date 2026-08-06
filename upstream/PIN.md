# 上游版本钉扎

```
STATUS: E1=PASS(LE YE2) · CLAIM-C-REAL(hybrid)=YES · CLAIM-B=未勾 · 正式上线=否
DATE: 2026-08-06
ONE_LINE: 证书已绿(LE DNS-01)；可谈 CLAIM-B；未自动正式上线
```

| 组件 | 版本 | 日期 | 备注 |
|------|------|------|------|
| **Dify** | `1.16.1` | 2026-08-05 | workbench · Chat `lOMVPbz7rZmbJSJl` |
| DeepSeek | `deepseek-chat` | 2026-08-05 | 默认 LLM |
| **TLS** | **Let's Encrypt YE2** | 2026-08-06 | `workbench.aivia.asia` · DNS-01 acme.sh · ~2026-11-03 |
| **bridge** | **`0.2.0` MODE=hybrid** | 2026-08-06 | host + `aivia-bridge` 容器 |
| OpenWork | 二期 | | 非主线 |

> 密钥 / IP / SSH **不进本文件**。

## E1 出口

| 项 | 结果 |
|----|------|
| 浏览器无证书警告 | **YES**（系统校验 VERIFY_OK） |
| CA | **Let's Encrypt YE2** |
| Chat HTTPS | **200** |
| G1 下载 | **PASS** |
| **E1** | **PASS** |
| **CLAIM-B** | **未勾**（可谈，另验收） |

## C-REAL 出口

| 项 | 结果 |
|----|------|
| **CLAIM-C-REAL(hybrid)** | **YES** |
| CLAIM-C-REAL full | **NO** |

## D-PILOT-LITE 出口

| 项 | 结果 |
|----|------|
| **CLAIM-D-LITE** | **YES** |
