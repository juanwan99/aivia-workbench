# 上游版本钉扎

```
STATUS: CLAIM-C-REAL(hybrid)=YES · E1=BLOCKED · CLAIM-B=NO · 正式上线=否
DATE: 2026-08-06
ONE_LINE: bridge hybrid 0.2.0+工具绿；证书仍自签；不可 CLAIM-B
```

| 组件 | 版本 | 日期 | 备注 |
|------|------|------|------|
| **Dify** | `1.16.1` | 2026-08-05 | workbench · Chat `lOMVPbz7rZmbJSJl` · `127.0.0.1:13080` |
| DeepSeek | `deepseek-chat` | 2026-08-05 | 默认 LLM |
| **bridge** | **`0.2.0` MODE=hybrid** | 2026-08-06 | 主机 + Docker `aivia-bridge`（dify_default）· exchange token 强制 · fixture |
| SSRF 例外 | aivia-bridge 域名 + 容器 IP | 2026-08-06 | 仅 `.env`；无密钥进仓 |
| OpenWork | 二期 | | 非主线 |

> 密钥 / IP / SSH **不进本文件**。

## E1 出口

| 项 | 结果 |
|----|------|
| 浏览器无证书警告 | **NO（自签）** |
| DNS-01 / 云证书 | **BLOCKED** |
| **E1** | **BLOCKED** |
| **CLAIM-B** | **NO** |

## C-REAL 出口

| 项 | 结果 |
|----|------|
| MODE | **hybrid** |
| smoke | **13/13** |
| Dify `list_my_classes` | **PASS** |
| **CLAIM-C-REAL(hybrid)** | **YES** |
| CLAIM-C-REAL full | **NO** |
| **CLAIM-B** | **NO** |

## D-PILOT-LITE 出口

| 项 | 结果 |
|----|------|
| **CLAIM-D-LITE** | **YES** |
| 进仓证据 | `ops/evidence/d-pilot-lite/` |
