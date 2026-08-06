# 债务总账

```
UPDATED: 2026-08-06 · CLAIM-WB-FIX-DEPLOY=YES
```

| 项 | 状态 |
|----|------|
| WB-ALIGN | **有条件绿 → FIX 消化后仍保留跳过项** |
| **WB-FIX-DEPLOY** | **PASS · CLAIM-WB-FIX-DEPLOY=YES** |
| R1 真上传 | **关**（API 上传再加工已演示） |
| R2 交付清单 | **关** |
| R3 DOCX 稳 | **关**（×2 OOXML） |
| R4 弱大纲 | **关** |
| R5 TLS 边缘 | **说明中**（源站 OK · 客户端 schannel 可能失败） |
| R6/R8 ops 部署烟测 | **关**（0.2.2 + metrics/policy） |
| 正式上线 | **否** |
| 专家壳 / full real | **后置** |
| HTML 模型 fence 波动 | **观察**（重试可绿） |

卡：`ops/TASK-CARD-WB-FIX-DEPLOY.md` · 报告：`ops/WB-FIX-DEPLOY-REPORT.md`
