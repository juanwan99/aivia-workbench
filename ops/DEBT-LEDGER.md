# 债务台账（摘要）

```
UPDATED: 2026-08-06
```

| 债 | 状态 |
|----|------|
| E1 正式证书 | **BLOCKED**（DNS-01 待业主；仍自签） |
| CLAIM-B | **NO**（绑 E1） |
| edu live 只读 | **后置**（BFF 仅 health）→ 现 **hybrid** |
| CLAIM-C-REAL(hybrid) | **YES** |
| CLAIM-D-LITE | **YES** |
| Dify SSRF 私网 | 已放行 aivia-bridge / bridge IP（运维 .env） |

禁止：E1 未过勾 CLAIM-B；hybrid 说成 full real。
