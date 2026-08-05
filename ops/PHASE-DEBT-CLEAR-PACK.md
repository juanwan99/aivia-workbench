# 阶段 DEBT-CLEAR 执行包（债务清零 + 优化完备）

```
STATUS: BINDING · 债务清零唯一执行包
DATE: 2026-08-05
对齐: CANON · HANDOFF · PHASE-B-CLOSEOUT · B-HARDEN-RUNBOOK · INFRA
目标: 清零 A/B/Harden 残留债务；E1 满后方可谈教师正式使用
对标: 无警告打开 + 真下载 + 配额 + 诚实失败
```

> 先读 [`docs/CANON.md`](../docs/CANON.md)。**不重做 A/B**；应用硬化（H1/H3/H7）已绿。  
> 勾选清单：[`ops/DEBT-CLEAR-RUNBOOK.md`](./DEBT-CLEAR-RUNBOOK.md)

---

## 0. 债务表 → 执行项

| 债 | 执行 | 优先级 | 可后置？ |
|----|------|--------|----------|
| D1/D2 自签 + 公网阻断 | **E1** 正式证书 + 公网非 403 | **P0** | **否**（CLAIM-B 门） |
| D3 日配额虚 | **E2** 日消息/token 或等价 + 超限人话 | P1 | 仅账单级可后置并书面 |
| D4/D6 附件/大文件 | **E3** storage 升档或 data-URL 正式 + 大文件策略 | P1 | storage 可后置；策略必写 |
| D5/D9 教案 DOCX | **E4** DOCX 或 **永久 MD** + skills 名实 | P1 | DOCX 可永久后置 |
| D7 知识库 | **E5** embedding 或 economy 永久 | P2 | 可书面 economy |
| D8 证据 | **E6** 抽检证据 | P2 | 否（本阶段必记） |
| D10/D11 治理 | **E0** 真源扫尾 | P0 文档 | 否 |
| D12 运维 | **E7** 备份/磁盘/Pico | P2 | 否（本阶段必记） |
| 回归 | **E8** V1–V8 空成功 0 | P0 出口 | 否 |

---

## 1. CLAIM 分层

| CLAIM | 条件 |
|-------|------|
| **CLAIM-A 债务清零** | **E1 必满**；E2–E7 做完或**书面后置**（仅允许 P2/策略项） |
| **CLAIM-B 教师正式可用** | **仅** E1 满 + 默认 Chat 可打开 + 下载可用 |
| 阶段 C | **另授权** · 本包不做 |

**禁止：** E1 未满宣称教师正式上线；重刷完整 B；OpenWork 主线；动 Dify 核。

---

## 2. 工作包

### E0 · 真源扫尾

- [ ] 本 PACK + DEBT-CLEAR-RUNBOOK 落盘  
- [ ] CANON / HANDOFF / README / PIN / INFRA 指向 DEBT-CLEAR  
- [ ] Issue #1 标题/评论与本包一致  

### E1 · 正式证书 + 公网（P0）

```text
[ ] 浏览器无证书警告打开 https://workbench.aivia.asia
[ ] 公网可开默认 Chat（非 403）
[ ] 优先：DNS-01（阿里云 DNS）或云厂商证书
[ ] 备选：HTTP-01（历史：外网 LE 校验 403 / 空 body；需 WAF 放行）
[ ] Issue 留「E1 PASS」或「E1 BLOCKED + 解锁步骤」
```

**现网事实（2026-08-05 执行窗）：**

- 证书仍为**自签**（CN=workbench.aivia.asia）  
- 本机/环回访问 ACME webroot **有 body**；**外网 LE 校验点返回 403/空 body**  
- HTTP-01 在现网 **不可靠** → **必须 DNS-01 或平台证书**  
- 无 ECS 上阿里云 DNS AK（策略禁止长驻 AK）；需业主 DNS API 或手工 TXT  

### E2 · 日配额

| 旋钮 | 试点起点（可调，须记 Issue） |
|------|------------------------------|
| 并发 | `max_active_requests=8`（已 Harden） |
| 频控 | nginx `30r/m/IP` burst 20（已 Harden） |
| 日 token/消息账单级 | **可后置**，须书面；超限人话已有 429 JSON |

**验收：** 配置数字进 Issue；至少一次超限/失败人话可演示。

### E3 · 附件 / 大文件

| 选项 | 说明 |
|------|------|
| **正式 data-URL**（现行） | Code 节点 `DOWNLOAD_READY` + 点击下载；满足 CLAIM-B 下载门 |
| storage 附件升档 | 后置；勿 fork 核 |
| 大文件 | `client_max_body_size 100M`；课件建议 &lt;2MB；过大拆分/压缩 |

禁止口头说「平台附件」而实际仅代码墙。

### E4 · 教案

- **永久 scope（v0.x）：Markdown only**  
- DOCX 后置；`skills/lesson-plan-docx` 已写明  
- 禁止终态写「已生成 Word」  

### E5 · 知识库

- 现行：`Aivia课件结构模板` · **economy**  
- 无 embedding 前 **economy 为永久口径**；上 embedding 再升 high_quality  

### E6 · 证据

- 服务器产物目录抽检 ≥2 HTML + 1 教案 MD  
- 元数据进 Issue；全文不进 Git  

### E7 · 运维

- 磁盘余量、Pico 仍可访问、备份策略一句  
- 禁止无备份拆 Pico 域名  

### E8 · 总回归 V1–V8

| # | 话术意图 | 期望 |
|---|----------|------|
| V1 | 新主题 HTML 下载 | DOWNLOAD_READY |
| V2 | 同会话改稿 | 仍有文件 |
| V3 | 只要大纲 | 无假文件 |
| V4 | 故意不可能任务 | 明确失败 |
| V5 | 极短「课件」 | 出件或澄清 1 次后出件 |
| V6 | 教案 MD | 可下载/完整 MD |
| V7 | 教案改稿 | 仍有产物 |
| V8 | 另一主题 HTML | DOWNLOAD_READY |

**空成功 = 0。**

---

## 3. 完成定义

```text
[ ] E0 真源同步
[ ] E1 正式证书无警告 + 公网可开  —— CLAIM-B 门
[ ] E2 配额口径书面 + 超限人话
[ ] E3 出件形态书面（data-URL 正式 / storage 后置）+ 大文件策略
[ ] E4 MD 永久或 DOCX 实做
[ ] E5 economy 永久或 embedding
[ ] E6 证据记录
[ ] E7 运维记录
[ ] E8 空成功 0
[ ] RUNBOOK + PIN + Issue 回写（无 Key / 无公网 IP）
```

---

## 4. 不做

- 重装 Dify / 重刷完整 10 次 B  
- OpenWork 主线  
- 未授权 C / edu 写库  
- E1 未满假上线  
- 密钥进仓  

## 5. 关联

| 文件 | 用途 |
|------|------|
| `ops/DEBT-CLEAR-RUNBOOK.md` | 勾选 |
| `ops/PHASE-B-CLOSEOUT.md` | Harden 残留 |
| `ops/B-HARDEN-RUNBOOK.md` | H1/H3/H7 已绿 |
| `ops/INFRA.md` | 证书/域名 |
| `upstream/PIN.md` | 版本钉 |
