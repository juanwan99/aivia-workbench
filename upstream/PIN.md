# 上游版本钉扎

```
主线组件：Dify（Web）
OpenWork：optional / 二期
STATUS: A 功能绿 · B 电池有条件 M3 · Harden 应用绿 · DEBT-CLEAR 应用侧 E2–E8 · E1 证书 BLOCKED
```

| 组件 | 版本 / 镜像 tag | 日期 | 备注 |
|------|-----------------|------|------|
| **Dify** | `1.16.1`（compose project `dify`） | 2026-08-05 | 入口 **https://workbench.aivia.asia** · 默认 Chat `.../chat/lOMVPbz7rZmbJSJl` · 本机 `127.0.0.1:13080` |
| DeepSeek 模型 id | `deepseek-chat`（插件 `langgenius/deepseek` `0.0.19`） | 2026-08-05 | 默认 LLM |
| OpenWork（optional） | _二期再填_ | | 非主线 |

> **安全：** 公网 IP / SSH / 面板 **不进本文件**。

## 阶段 A 摘要

G0/G0b/G1/G1+ PASS · G4 在 B0/Harden 补测 PASS · HTTPS **临时自签**

## 阶段 B 摘要

10 次电池空成功 **0** · B0–B5（B3 后 Harden 升格）· 见 `ops/B-PATH-RUNBOOK.md`

## 阶段 B-HARDEN 出口（2026-08-05）

| 项 | 结果 |
|----|------|
| H1 真下载 | **PASS** · Chatflow Code 节点 → `DOWNLOAD_READY` + data-URL |
| H2 证书/公网 | **并入 E1** · 自签仍在 |
| H3 配额 | **PASS** · max_active_requests=8 + nginx 30r/m/IP |
| H4 教案 | **MD only** |
| H5 单入口 | **PASS** |
| H7 回归空成功 | **0** |

## 阶段 DEBT-CLEAR 出口（2026-08-05）

| 项 | 结果 |
|----|------|
| E1 正式证书 | **BLOCKED** · HTTP-01 外网 LE **403/空 body**；需 **DNS-01** 或云厂商证书 |
| E2 日配额 | **PASS** · 并发8 + nginx 30r/m + 429 人话；账单级日 token **后置书面** |
| E3 附件/大文件 | **PASS** · data-URL 正式；storage 后置；body 100M / 课件建议 &lt;2MB |
| E4 教案 | **PASS** · 永久 MD only |
| E5 知识库 | **PASS** · economy 永久（无 embedding） |
| E6 证据 | **PASS** · `/home/ops/aivia-phase-debt-clear/` + harden/b 产物 |
| E7 运维 | **PASS** · Pico 200；磁盘约 84%（告警）；nginx 事故后已恢复 |
| E8 V1–V8 | **PASS · 空成功 0** |
| CLAIM-A | **NO**（E1 未满） |
| CLAIM-B | **NO**（E1 未满） |

**下一刀：** 阿里云 DNS 编辑（API 或手工 TXT）完成 E1 → 方可 CLAIM-B。  
