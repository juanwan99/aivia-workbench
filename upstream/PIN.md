# 上游版本钉扎

```
STATUS: CLAIM-S4-CAP=FULL YES · CLAIM-S4.1-HOTFIX=YES · CLAIM-S3-UX=YES · CLAIM-GENERAL-WB=FULL YES · 产品主线=GENERAL-WB
DATE: 2026-08-06
ONE_LINE: CLAIM-S4-CAP FULL（S4.1 关 C2 套娃债：真 csv 再加工·防清单入表）；下一刀 维护态/业主点名
```

| 组件 | 版本/值 | 备注 |
|------|---------|------|
| Dify | 1.16.1 | Chat `lOMVPbz7rZmbJSJl` |
| DeepSeek | 默认 LLM | |
| **App / site.title** | **Aivia 通用 Agent** | |
| **workflow** | **general-wb-s4.1** | 见 `ops/evidence/general-wb/s4.1/general-wb-s4.1-wf-id.txt` |
| PackDownload | **s4.1** multi+anti-nest | 双产物；拒交付清单套娃 sheet |
| bridge | 0.2.2 hybrid | PUBLIC_DL=`asyncova.com/dl` |
| **CLAIM-S4.1-HOTFIX** | **YES** | F1–F7 · `ops/evidence/general-wb/s4.1/` |
| **CLAIM-S4-CAP** | **FULL YES** | S4 + S4.1 |
| **CLAIM-S3-UX** | **YES** | U1–U7 · `ops/evidence/general-wb/s3/` |
| **CLAIM-GENERAL-WB** | **FULL YES** | S2 + S2.1 审查债关 |
| **CLAIM-S2.1-HOTFIX** | **YES** | `ops/evidence/general-wb/s2.1/` |
| **CLAIM-S1 / S1.1** | YES | |
| **/experts 口径** | 行为对标 · ≠像素 · ≠备案完成 | `deploy/aivia-experts/index.html` |

### 入口说明

| 用途 | URL |
|------|-----|
| 公司站根域 | https://asyncova.com/ |
| **工作台 Chat** | https://asyncova.com/chat/lOMVPbz7rZmbJSJl |
| 能力目录 | https://asyncova.com/experts |
| 下载 | https://asyncova.com/dl/{id}/file.{ext} |

> 根域 ≠ 工作台。密钥不进仓。
