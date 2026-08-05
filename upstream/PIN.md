# 上游版本钉扎

```
STATUS: CLAIM-C + CLAIM-C-FIX 绿(mock) · E1 后置 · CLAIM-B NO
DATE: 2026-08-06
```

| 组件 | 版本 | 日期 | 备注 |
|------|------|------|------|
| **Dify** | `1.16.1` | 2026-08-05 | workbench · Chat `lOMVPbz7rZmbJSJl` · `127.0.0.1:13080` |
| DeepSeek | `deepseek-chat` | 2026-08-05 | 默认 LLM |
| **bridge** | **`0.1.1` MODE=mock** | 2026-08-06 | `127.0.0.1:18090` · **systemd --user aivia-bridge** · JWT 强密钥 · exchange token |
| 部署 | systemd user | 2026-08-06 | `EnvironmentFile=~/.secrets/bridge.env` · Restart=on-failure |
| OpenWork | 二期 | | 非主线 |

> 密钥 / IP / SSH **不进本文件**。

## C-FIX-DEPLOY 出口

| 项 | 结果 |
|----|------|
| F1 弱 secret 拒启 | **PASS** |
| F1 exchange token | **PASS**（401 on bad） |
| F2 Dify 挂载 | **书面后置** |
| F3 smoke | **PASS** 11/11 |
| D1 systemd 复活 | **PASS** |
| D2 仅 loopback | **PASS** |
| R2 G1 | **PASS** |
| **CLAIM-C-FIX** | **YES** |
| **CLAIM-B** | **NO** |
