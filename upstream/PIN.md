# 上游版本钉扎

```
主线组件：Dify（Web）
OpenWork：optional / 二期
STATUS: A/B/Harden/DEBT应用侧 · C 绿(mock) · E1 后置 · CLAIM-B 否
```

| 组件 | 版本 / 镜像 tag | 日期 | 备注 |
|------|-----------------|------|------|
| **Dify** | `1.16.1` | 2026-08-05 | 入口 workbench · Chat `lOMVPbz7rZmbJSJl` · 本机 `127.0.0.1:13080` |
| DeepSeek | `deepseek-chat` | 2026-08-05 | 默认 LLM |
| **bridge** | `0.1.0` MODE=**mock** | 2026-08-05 | `127.0.0.1:18090` · JWT HS256 · SQLite 提案 |
| OpenWork | _二期_ | | 非主线 |

> **安全：** 公网 IP / SSH / 面板 / JWT secret **不进本文件**。

## 阶段 C 出口（2026-08-05）

| 项 | 结果 |
|----|------|
| MODE | **mock**（edu-core 业务 API 未挂；同契约） |
| Principal | PASS · exchange + /me + exp 401 |
| 只读 ×2 | PASS · classes + course meta |
| 跨校 | PASS · 403 |
| 提案 | PASS · pending；**无 apply** |
| 人审 | PASS · reject + approve |
| 审计 | PASS · audit.jsonl 脱敏 |
| G1 回归 | PASS · DOWNLOAD_READY |
| **CLAIM-C** | **YES（mock）** |
| **CLAIM-B** | **NO**（E1 后置） |

证据：`/home/ops/aivia-phase-c-artifacts/phase-c-meta.json`  
