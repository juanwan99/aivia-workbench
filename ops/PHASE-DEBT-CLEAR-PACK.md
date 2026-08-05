# 债务清零 + 优化完备包（H2 与后 Harden 全量）

```
STATUS: BINDING · 当前唯一执行包
DATE: 2026-08-05
CODE: PHASE-DEBT-CLEAR / PROD-READY-LITE
对齐: CANON · PHASE-B-CLOSEOUT · B-HARDEN 审查
前提: A 功能绿 · B 电池空成功0 · 应用硬化 H1/H3/H7 绿
出口: 债务表全关或书面永久后置 · 可「知悉风险的小范围试用」或「正式证书下教师可用」分层 CLAIM
```

> **不要**重装 Dify、重刷完整 10 次 B、开未授权 C、OpenWork 主线。  
> **要**把审查留下的债与优化项一次做完或显式关闭。

---

## 0. 债务总表（本包范围 = 全部未清项）

| ID | 债务/优化 | 优先级 | 包 | 关闭标准 |
|----|-----------|--------|-----|----------|
| **D1** | 正式 HTTPS（去自签警告） | P0 | E1 | 浏览器无证书警告打开 workbench |
| **D2** | 公网可达（清 Beaver/WAF 403） | P0 | E1 | 外网浏览器能开默认 Chat 并完成一轮短聊 |
| **D3** | 日级配额（消息或 token 账单封顶） | P1 | E2 | 有数字 + 超限人话一次 |
| **D4** | 平台 storage/附件出件（补强 data-URL） | P1 | E3 | 至少 HTML 走文件变量/附件下载一条路径 |
| **D5** | 教案真 DOCX | P1 | E4 | T4 类话术出 `.docx` 可下载 **或** 永久 MD-only 钉死并改名 skills |
| **D6** | 大课件 data-URL 体积风险 | P1 | E3 | 超限失败人话；大文件走附件路径 |
| **D7** | 知识库 embedding/高质量检索 | P2 | E5 | 有 embedding 模型并挂库 **或** 书面 economy 永久 |
| **D8** | 产物抽检可追溯（样例/清单） | P2 | E6 | Issue 或 `ops/fixtures` 脱敏记录 |
| **D9** | skills 名实（docx 目录实际 MD） | P2 | E4 | 改名或 README 大字声明 |
| **D10** | HARDEN-PACK 模板勾选残留误导 | P2 | E0 | 扫尾与 CLOSEOUT 一致 |
| **D11** | Issue 历史 OpenWork/IP 污染 | P2 | E0 | 置顶真源评论；不删履历 |
| **D12** | 备份/磁盘/Pico 共存 | P2 | E7 | 备份策略一句话 + 磁盘余量检查 |
| **OUT** | 阶段 C edu | — | **不做** | 须另授权另卡 |
| **OUT** | OpenWork 主线 | — | **不做** | 二期 |

---

## 1. 工作包（按序；可同日串行）

### E0 · 治理扫尾（30–60 min）

1. Issue #1 置顶/最新评论：现行下一刀 = 本包；旧 OpenWork 评论仅履历  
2. `PHASE-B-HARDEN-PACK` 顶部加 STATUS：应用硬化已完成，剩余见本包  
3. 确认 CANON/HANDOFF 指向 `PHASE-DEBT-CLEAR-PACK`  

### E1 · 入口生产化（D1+D2 · P0 · 必须）

**证书（D1）**

- DNS-01（推荐，绕开 HTTP-01 403）或云厂商证书挂到 workbench 反代  
- 验收：Chrome/Safari **无**「不安全/自签」警告  

**公网（D2）**

- 放行 WAF/Beaver：Host `workbench.aivia.asia`、必要 path、健康检查  
- 验收：
  1. 外网 `https://workbench.aivia.asia/` 非 403  
  2. 打开 `.../chat/lOMVPbz7rZmbJSJl` 能对话  
  3. 短聊 G0b 或一句话要课件仍可下载  

**E1 绿** = D1+D2 全过 → 才允许「教师正式使用」话术。  
**E1 失败** = 保持「内测/自签范围」，不得假绿。

### E2 · 账单级配额（D3 · P1）

在现有 `max_active_requests=8` + nginx 30r/m 之上增加至少一项：

| 选项 | 示例起点（可调，记 Issue） |
|------|---------------------------|
| 工作空间/应用日消息上限 | 如 200～500 条/日 |
| 用户级日限额（若 Dify 支持） | 试点数字 |
| 超限文案 | 「今日额度已用完，请联系管理员」 |

验收：配置落盘（无密钥）+ **触发或模拟一次**超限人话。  
与 H3 关系：H3=防打爆；E2=防烧钱。

### E3 · 交付路径升档（D4+D6 · P1）

目标：减少对「巨型 data-URL」的依赖。

1. 调研 Dify 1.16 Chatflow 文件变量 / 工具写文件 / 消息附件  
2. 实现 **一条** HTML → 平台文件或可点附件下载主路径  
3. data-URL 可保留为降级  
4. 超大输出：明确失败或切附件，禁止静默截断装成功  

回归：R1（新下载路径）+ R2 改稿 + 一次故意超大/失败。

### E4 · 教案 DOCX 或永久 MD（D5+D9 · P1）

**二选一（必须选，禁止含糊）：**

- **路径甲：** 出可下载 `.docx`（转换节点或工具），T4 回归 PASS  
- **路径乙：** 永久 v0.x=MD；更新 `skills/lesson-plan-docx` 为 lesson-plan（或 README 大字「非 DOCX」）；CANON 一句  

### E5 · 知识库（D7 · P2）

- 配 embedding（若有 DeepSeek/其它 embedding 可用）→ high_quality 库  
- 或书面：**economy 永久**，模板靠系统提示  

### E6 · 证据（D8 · P2）

- Issue 表：样例文件名 + 可开 + 下载方式（data-URL/附件）  
- 可选：`ops/fixtures/sample-courseware-shell.html` 无版权壳  

### E7 · 运维稳态（D12 · P2）

- 磁盘余量、Docker 日志轮转、Pico 域名仍在、备份是否存在（有/无/计划）  
- 禁止无备份拆 pico  

### E8 · 总回归（债务清零验收）

| # | 项 | 过线 |
|---|-----|------|
| V1 | 无证书警告打开默认 Chat | E1 |
| V2 | 外网非 403 | E1 |
| V3 | 一句话课件真下载 | E3/H1 |
| V4 | 改稿仍有文件 | |
| V5 | 失败不假绿 | |
| V6 | 超限/配额人话（若 E2 做了） | |
| V7 | 教案路径与书面 scope 一致 | E4 |
| V8 | 空成功（本回归）= 0 | |

---

## 2. 完成定义（分层 CLAIM）

### CLAIM-A · 债务清零（本包绿）

```text
[ ] E0 治理扫尾
[ ] E1 D1+D2 PASS（正式证书 + 公网可聊）
[ ] E2 日配额 PASS 或书面「试点前数字」+ 临时沿用 H3（须 Issue 钉死日期）
[ ] E3 附件路径 PASS 或书面「data-URL 为正式主路径」+ 大文件失败策略
[ ] E4 DOCX 或永久 MD 钉死
[ ] E5/E6/E7 做完或书面后置
[ ] E8 V1–V8 空成功 0
[ ] PIN + DEBT-CLEAR-RUNBOOK + Issue 回写
[ ] 未宣称 C；无密钥/IP 进仓
```

### CLAIM-B · 教师正式可用（更严）

- CLAIM-A 中 **E1 必须满**  
- 默认 Chat 无警告、外网可进、下载可用  
- 仍 **不含** edu 身份（C）  

### 允许的「书面永久后置」（须进 CLOSEOUT）

仅限 P2：embedding、fixtures、DOCX（若选乙）、storage 附件（若选 data-URL 正式）。  
**D1/D2 不允许永久后置。**

---

## 3. 禁止

- 重装 Dify / 重刷 10 次 B 刷指标  
- OpenWork 主线 / 双入口  
- 未授权 C  
- E1 未过宣称教师正式上线  
- 密钥、公网 IP 进 Git  

---

## 4. 关联

| 文件 | 用途 |
|------|------|
| `ops/DEBT-CLEAR-RUNBOOK.md` | 勾选 |
| `ops/PHASE-B-CLOSEOUT.md` | 历史残留 |
| `ops/PHASE-A-CLOSEOUT.md` | 证书同源 |
| `ops/INFRA.md` | 域名/反代 |
| `upstream/PIN.md` | 出口 |
