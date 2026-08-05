# 上游版本钉扎

```
主线组件：Dify（Web）
OpenWork：optional / 二期
STATUS: A 功能绿 · B 纪律电池有条件绿 · B 硬化 OPEN · 见 PHASE-B-CLOSEOUT
```

| 组件 | 版本 / 镜像 tag | 日期 | 备注 |
|------|-----------------|------|------|
| **Dify** | `1.16.1`（compose project `dify`） | 2026-08-05 | 镜像 `langgenius/dify-api:1.16.1` / `langgenius/dify-web:1.16.1` · 入口 **https://workbench.aivia.asia**（本机反代 `127.0.0.1:13080`） |
| DeepSeek 模型 id | `deepseek-chat`（插件 `langgenius/deepseek` `0.0.19`） | 2026-08-05 | 默认 LLM |
| OpenWork（optional） | _二期再填_ | | 非主线 |

> **安全：** 公网 IP / SSH / 面板 **不进本文件**。

## 阶段 A 验收摘要（无密钥）

| 项 | 结果 |
|----|------|
| G0 / G0b / G1 / G1+ | **PASS** |
| 默认入口（历史） | Aivia 课件（阶段A）agent · `dV3HeqgfVt4Xmm7f` |
| G4 | **PASS**（B0 补测） |
| HTTPS | **临时自签** · 待正式证书 |
| 公网可达 | **有隐患** · 外网曾 403 |

## 阶段 B 出口（2026-08-05 · 纪律电池）

| 项 | 结果 |
|----|------|
| 默认应用 | **Aivia 课件** Chatflow · `https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl` |
| 10 次电池空成功 | **0** |
| B0 / B1 / B2 / B4 / B5 | **PASS** |
| **B3 配额** | **PARTIAL** · 仅有 max_tokens/temperature 起点；**真日配额见 Harden H3** |
| 交付形态 | **代码块/另存为主** · 平台附件见 Harden H1 |
| 教案格式 | **MD** · DOCX 见 Harden H4 |
| 产物目录 | 服务器 `/home/ops/aivia-phase-b-artifacts/`（无 Key） |

## 阶段 B 硬化（OPEN）

见 `ops/PHASE-B-HARDEN-PACK.md` · `ops/PHASE-B-CLOSEOUT.md`。  
Harden 绿前：禁止对外「教师正式可用」；禁止无授权开 C。

更新主线上游前：跑浏览器回归，失败则回退 PIN。
