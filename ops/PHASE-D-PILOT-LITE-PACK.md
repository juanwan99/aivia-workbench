# 阶段 D · 轻量内测试点（PILOT-LITE）

```
STATUS: BINDING · 阶段 D 轻量试点唯一执行包
CODE: PHASE-D-PILOT-LITE
DATE: 2026-08-06
对齐: CANON · HANDOFF · DELIVERY-RULES · PROJECT-PLAN
前提: A/B/Harden/DEBT 应用侧绿 · CLAIM-C/C-FIX 绿(mock) · 课件已知可出件
出口: ≥3 会话记录 + 短报告 + 下一刀 · CLAIM-D-LITE
对标: 产品/运营轻量内测 · 非全校 · 非正式上线
```

> **新窗：** 先读本文全文 + [`D-PILOT-RUNBOOK.md`](./D-PILOT-RUNBOOK.md)。  
> **真源顺序：** 本 PACK → RUNBOOK → 会话产物 → 短报告。

---

## 0. 本阶段解决什么

正式 **D 试点（M5）** 在 PROJECT-PLAN 中挂在 **E1 绿后**。  
**PILOT-LITE** 是 E1 未解前的 **受控轻量内测**：用现网默认入口验证「产品路径仍可出件、改稿、诚实失败」，给产品/运营留会话证据，**不**宣称教师正式可用。

| 用户/业主真相 | PILOT-LITE 必须做到 |
|---------------|---------------------|
| 课件链路还活着吗 | ≥3 真实会话有记录 |
| 一句话要文件 | HTML / 教案可下载（DOWNLOAD_READY 优先） |
| 改一版还有文件吗 | 至少 1 次同会话改稿 |
| 不要文件时会不会假绿 | 大纲类请求不出「假成功文件」 |
| 能对外宣布上线吗 | **不能**（CLAIM-D-LITE ≠ CLAIM-B） |

---

## 1. 硬约束（不可谈判）

| 做 | 不做 |
|----|------|
| 默认入口 Chat 内测 | 全校推广 / 对外「正式上线」话术 |
| 知悉自签证书警告 | **E1** 正式证书（本包不做） |
| 课件/教案产品路径 | **接 edu real** / 改 bridge MODE |
| 保留限流与配额 | 关限流刷数 |
| 会话证据 + 短报告 | 重刷完整 B 10 次电池 |
| CLAIM-D-LITE | **CLAIM-B** |

**CLAIM-D-LITE 定义：**  
试点会话完成且空成功=0（要文件场景）→ 可报 **轻量内测完成**。  
**明确不等于** 正式上线、不等于 CLAIM-B、不等于 M5 全量试点。

---

## 2. 入口与环境

| 项 | 值 |
|----|-----|
| 默认入口 | `https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl` |
| 环回（运维） | `http://127.0.0.1:13080` · Dify 1.16.1 |
| 应用 | Aivia 课件 · advanced-chat |
| 证书 | 自签 · **已知警告** · 内测可接受 |
| edu 桥 | 不调用；MODE=mock 保持；本包不接 real |
| 产物目录（进仓） | `ops/evidence/d-pilot-lite/` |
| 服务器镜像（非仓） | `/home/ops/aivia-phase-d-pilot-lite/` |

---

## 3. 工作包

### D0 · 开场门禁（轻）

- [ ] 入口可打开（自签警告记一笔即可）  
- [ ] 公开 Chat `enable_site=true` · passport 可取  
- [ ] **不**关 nginx 限流、**不**改 max_active_requests 刷数  

### D1 · 会话电池（≥3 会话）

| ID | 场景 | 期望 |
|----|------|------|
| S1 | 一句话 HTML 课件 | DOWNLOAD_READY / 可下载 · 结构底线 |
| S2 | 同会话改稿再导出 | 仍有文件 |
| S3 | 教案 Markdown | 可下载 md · 非假 Word |
| S4（推荐） | 只要大纲不要文件 | 无 DOWNLOAD_READY 假绿 |

计分：

- **空成功：** 要文件场景无产物却当成功 → 计 FAIL  
- **质量：** HTML 可开、有标题/结构、非半截  
- **会话数：** 独立 conversation ≥3（S2 多轮算 1 会话）  

### D2 · 轻运维观察（只读）

- bridge health（可选，本包不测 Ce 全套）  
- 磁盘/进程不在本包扩 scope；异常只记备注  

### D3 · 交付物

| 产物 | 路径 |
|------|------|
| 会话 meta（进仓） | `ops/evidence/d-pilot-lite/pilot-meta.json` |
| 产物文件（进仓） | `ops/evidence/d-pilot-lite/s*-artifact.*` |
| RUNBOOK 勾选 | `ops/D-PILOT-RUNBOOK.md` |
| 短报告 | `ops/D-PILOT-LITE-REPORT.md` |
| 真源回写 | CANON / HANDOFF / README / PIN / PROJECT-PLAN |
| Issue 回写 | Issue #1 评论（无密钥） |
| 远端 | push `main` |

---

## 4. 出口门禁

全部满足才可勾 **CLAIM-D-LITE**：

1. RUNBOOK 会话表 ≥3 行有 conversation_id  
2. 要文件场景 **空成功 = 0**  
3. 短报告含：结果摘要、风险、**下一刀**  
4. 全文 **无**「教师正式上线 / CLAIM-B / 全校推广」  

未满足 → 不宣称 D-LITE 绿；记 BLOCKED 原因。

---

## 5. 下一刀（PACK 默认建议 · 报告可细化）

按业主优先级择一（**互不假装已完成**）：

1. **E1 DNS-01** → 解 CLAIM-B 门（正式 HTTPS 无警告）  
2. **PHASE-C-REAL** → edu-core 只读白名单接真（仍 mock 提案人审）  
3. **D 全量试点（M5）** → 仅当 E1 绿后扩教师范围（非本包）  

---

## 6. 禁止清单（复读）

- 全校推广、CLAIM-B、关限流刷数  
- 接 edu real / 做 E1 / 密钥进仓  
- Agent 写成绩库  
- 用「试点完成」偷换「正式上线」
