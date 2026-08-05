# 上游版本钉扎

```
STATUS: CLAIM-D-LITE=YES · CLAIM-C/C-FIX=YES(mock) · E1后置 · CLAIM-B=NO · 正式上线=否
DATE: 2026-08-06
ONE_LINE: D-LITE 4会话空成功0已进仓；可内测不可正式上线
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

## D-PILOT-LITE 出口

| 项 | 结果 |
|----|------|
| 会话数 | **4**（≥3） |
| 空成功 | **0** |
| S1 HTML / S2 改稿 / S3 教案 / S4 大纲 | **全 PASS** |
| 产物（进仓） | `ops/evidence/d-pilot-lite/` |
| RUNBOOK / 报告 | `ops/D-PILOT-RUNBOOK.md` · `ops/D-PILOT-LITE-REPORT.md` |
| **CLAIM-D-LITE** | **YES** |
| 正式上线 / CLAIM-B | **NO** |

