# 上游版本钉扎

```
主线组件：Dify（Web）
OpenWork：optional / 二期
STATUS: A 功能出口 · B 电池有条件 M3 · B-HARDEN 应用硬化绿(H1/H3/H7) · H2 证书未满
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
| H1 真下载 | **PASS** · Chatflow Code 节点 → `DOWNLOAD_READY` + data-URL 点击下载 |
| H2 证书/公网 | **范围限制** · 自签仍在；正式证书待 DNS-01 |
| H3 配额 | **PASS** · `max_active_requests=8` + nginx `30r/m/IP` + 失败人话 |
| H4 教案 | **MD only**（DOCX 后置） |
| H5 单入口 | **PASS** · 仅主推 Chatflow；Agent 公开关闭 |
| H7 回归空成功 | **0**（R1–R5） |
| 产物 | `/home/ops/aivia-phase-b-harden/` |

**CLAIM：** 应用硬化绿（H1+H3+H7）；**不可**教师正式上线直至 H2 满。  
