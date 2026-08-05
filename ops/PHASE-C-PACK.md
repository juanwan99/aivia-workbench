# 阶段 C · edu 身份桥（写实规划 + 执行包）

```
STATUS: BINDING · 业主 2026-08-05 授权开 C
CODE: PHASE-C / EDU-BRIDGE
对齐: CANON · ARCHITECTURE L7 · CHANGE-POLICY · DELIVERY-RULES
前提: A/B 应用侧已收；E1 证书后置（C 可设计/原型，正式校外部署仍建议 E1）
出口: 身份入会话可证 + 只读不越权 + 写库仅提案 + 金路径 Ce 绿
对标: 一线教育/协作台 · 行为 clean-room · 不抄闭源
```

> **硬约束（不可谈判）**  
> 1. **AI / Agent 不直写 edu 业务库**（成绩、学籍、排课等）  
> 2. 不乱 fork Dify 核  
> 3. 不拆 WorkBuddy / 不像素抄  
> 4. 密钥不进仓；school 数据脱敏进 Issue  
> 5. OpenWork 仍非主入口  

---

## 0. 阶段 C 解决什么（产品语言）

A/B 证明了：**陌生人也能用工作台出课件**。  
C 要证明的是：**老师带着「哪所学校、什么身份」进来**，AI 在**组织边界内**干活——像一线平台一样有租户、角色、审计，而不是匿名聊天框。

| 用户真相 | C 必须做到 |
|----------|------------|
| 我是某校老师 | 登录/桥接后会话带 `school_id` + 角色 |
| 别校数据看不见 | 默认隔离；工具带租户过滤 |
| AI 别乱改成绩 | **禁止直写**；变更只出「提案」待人审 |
| 能查一点业务上下文 | **只读** API/工具（授权范围） |
| 出事能追 | 桥接日志：谁、何时、调了什么 |
| 工作台仍是 Web | Dify 主入口不变；桥是侧车 |

---

## 1. 对标一线平台（行为 · clean-room）

不对标皮肤；对标 **身份 / 租户 / 权限 / 审计 / 人机边界**。

| 能力 | 一线常见做法（Google Workspace Edu / 企业 ChatGPT SSO / 钉钉宜搭·教育中台等） | 本仓落地（C） |
|------|-----------------------------------------------------------------------------|---------------|
| 统一登录 | SSO / OIDC / 校统一身份 | **C1** OIDC/JWT 或 edu 签发 token；原型可 Mock IdP |
| 组织上下文 | org / tenant 注入会话 | **C2** `school_id` + `membership` 入桥接会话与 Dify 用户元数据 |
| 角色 | teacher / admin / student | **C2** 角色枚举；应用按角色显隐工具 |
| 数据隔离 | 按 org 过滤 | **C3** 只读工具强制带 school_id；拒绝跨校 |
| AI 写业务 | 少见「模型直写核心库」；多为草稿/审批 | **C4** 仅 `Proposal`；人审后才进 edu |
| 审计 | admin audit log | **C5** bridge 访问日志（无密钥、可脱敏） |
| 连接器 | 官方 API + 范围授权 | **C3** 白名单 API；最小 scope |
| 失败诚实 | 未授权说清 | 工具 401/403 → 人话，不假成功 |

**明确不做（C 范围外）：**  
全量 SIS 同步、排课引擎、支付、像素级抄某产品、Agent 自动改成绩。

---

## 2. 目标架构（可落地）

```text
浏览器
  └─ Dify Web（主入口 workbench）
        │  会话 / 课件应用（已有）
        │
        ├─ 用户身份 ◄── bridge 交换 / 注入 metadata
        │                 (school_id, role, sub, exp)
        │
        └─ 工具调用 ──► bridge API（本仓 bridge/）
                            │
                            ├─ GET 只读 ──► edu-core（白名单）
                            └─ POST 提案 ──► bridge 提案表/队列
                                              └─ 人审后 ──► edu-core 写（非 AI）

edu-core = 业务真源（外仓/现网系统）
bridge   = 薄适配：鉴权、租户、限流、审计、提案
```

### 本仓目录

| 路径 | 职责 |
|------|------|
| `bridge/` | 侧车服务设计 + 接口契约 + 原型代码 |
| `docs/EDU-BRIDGE.md` | 身份模型与 API 契约（人读） |
| `ops/PHASE-C-PACK.md` | 本执行包 |
| `ops/C-PATH-RUNBOOK.md` | 勾选 |
| Dify | 自定义工具指向 bridge；用户字段/SSO 配置 |

### 技术选型建议（可替换，须 PIN）

| 件 | 建议 | 理由 |
|----|------|------|
| bridge 运行时 | Node 22 或 Python FastAPI 小服务 | 与现网 Docker 同机侧挂 |
| 鉴权 | JWT（edu 签发或 bridge 换票） | 无状态、易注入 |
| 与 Dify | OpenAPI 自定义工具 + 请求头透传 | 不改 Dify 核 |
| 提案存储 | 先 SQLite/Postgres 单表 `proposals` | 可迁 |
| 密钥 | 仅服务器 env | 禁止进 Git |

---

## 3. 身份与数据模型（最小）

```text
Principal:
  sub            # 稳定用户 id
  school_id      # 租户
  role           # teacher | school_admin | staff | (student 后置)
  display_name   # 可选
  exp            # 过期

Proposal:
  id, school_id, author_sub, type, payload_json
  status: draft | pending_review | approved | rejected | applied
  created_at, reviewed_by, review_note
```

**规则：**  
- 任何 bridge 业务调用无有效 Principal → 401  
- `school_id` 不匹配 → 403  
- `type=grade_write` 等敏感类 **仅 proposal**，无 apply 自动路径给 Agent  

---

## 4. 工作包（按序做实）

### C0 · 发现与冻结契约（1 次，必须先做）

1. 确认 **edu-core** 真实形态：是否有现成 OIDC/JWT/API？文档 URL？  
2. 列出 **可只读** 白名单（例：班级列表、课程名、教学大纲元数据——**无**成绩写）  
3. 列出 **禁止** Agent 触达的写接口  
4. 产出：`docs/EDU-BRIDGE.md` 契约 v0.1 + Issue 确认  

**若 edu-core 暂不可连：** 启用 **Mock IdP + Mock 只读 API**（同契约），标注 `MODE=mock`，仍须跑通 Ce 金路径。  
**禁止**因 edu 未就绪就空转只写文档不写 bridge。

### C1 · 身份接入（登录/换票）

| 交付 | 验收 |
|------|------|
| 登录或换票得到 JWT/Principal | 解码含 school_id + role |
| 过期拒绝 | exp 失效 → 401 |
| Dify 侧能关联用户 | 控制台或工具头可见身份字段（无密码） |

路径：  
- **优选：** edu OIDC → bridge 校验 → 会话 cookie/头  
- **原型：** `bridge` 发测试 JWT（仅内测密钥）  

### C2 · 会话注入与角色

| 交付 | 验收 |
|------|------|
| 每次工具调用带 Principal | 日志可查 school_id |
| 角色影响能力 | teacher 可提案；无 admin 不可「审批通过」API |
| 课件应用仍可用 | 身份失败时人话提示，不假出件成功 |

### C3 · 只读工具（edu 或 Mock）

至少 **2 个** 只读工具挂到 Dify（例）：

1. `list_my_classes` — 当前 school 下班级  
2. `get_course_meta` — 课程/大纲元数据  

验收：  
- 正确 school 有数据  
- 伪造/跨校 school_id → 403  
- 超时/下游挂 → 人话失败，不空成功  

### C4 · 变更提案（禁止直写）

| 交付 | 验收 |
|------|------|
| `create_proposal` 工具 | Agent 只能创建 pending 提案 |
| 管理端或 API `review_proposal` | **人** approved/rejected |
| `apply` 仅人工/独立 job | Agent **无** apply 工具 |
| 审计字段齐全 | author、时间、payload 摘要 |

示例提案类型（v0）：`lesson_plan_archive`（归档教案元数据）、`roster_note`（备注）——**不要**一上来做改成绩。

### C5 · 审计、限流、安全

- 访问日志：sub, school_id, path, status, latency（无 token 明文）  
- 限流：与工作台 nginx 策略协调  
- CORS/仅内网或反代路径 `/bridge`  
- 威胁：越权、重放、提示词骗写库 → 单测或清单自测  

### C6 · 金路径 Ce（阶段 C 出口）

| ID | 步骤 | 通过 |
|----|------|------|
| **Ce0** | 以测试教师身份进入工作台 | 有 Principal |
| **Ce1** | 要一份 HTML 课件（原 G1） | 仍可下载（身份不破坏出件） |
| **Ce2** | 调用只读工具取本班/本校上下文 | 数据与 school 一致 |
| **Ce3** | 跨校或无 token 调只读 | **失败诚实** |
| **Ce4** | 创建一条提案 | status=pending；**库表无业务直写** |
| **Ce5** | 人审拒绝或通过 | 状态变；仅 approved 后可人工 apply（若实现） |
| **Ce6** | 审计可查本次调用 | 日志或管理查询 |

**阶段 C 绿：** Ce0–Ce4 + Ce6 必过；Ce5 至少拒绝或通过一条。  
**仍不自动 = CLAIM-B**（教师对外正式）——E1 后置则对外话术仍受限。

---

## 5. 与 Dify 集成要点（不改核）

1. **自定义工具** OpenAPI → `https://workbench.../bridge` 或内网 `http://127.0.0.1:PORT`  
2. 工具鉴权：Header `Authorization: Bearer <user_jwt>` 或 Dify 用户 token 换票  
3. 系统提示追加：  
   - 需要学校上下文时先调只读工具  
   - **禁止声称「已写入成绩/学籍」**  
   - 变更只能 create_proposal  
4. 课件应用主路径保持；桥是增强不是替换  

---

## 6. 安全与合规清单

```text
[ ] 无 AI 路径直写 edu 写接口
[ ] school_id 强制
[ ] JWT 校验签名与 exp
[ ] 日志无密钥、无完整身份证号
[ ] 提案 payload 最小化
[ ] 生产前换掉 Mock 密钥
[ ] E1 未做前仅内网/内测传播 bridge URL
```

---

## 7. 里程碑与工期（写实）

| 包 | 内容 | 参考 |
|----|------|------|
| C0 | 契约 + edu/Mock 决策 | 1–2 日 |
| C1–C2 | 身份 + 注入 | 2–4 日 |
| C3 | 只读工具 ×2 | 2–3 日 |
| C4 | 提案 + 人审 | 2–4 日 |
| C5–C6 | 审计 + Ce 金路径 | 1–2 日 |

可并行：C0 文档与 bridge 骨架。  
**Mock 模式可先绿 Ce**；接真 edu 时回归 Ce2–Ce5。

---

## 8. 完成定义（CLAIM-C）

```text
[ ] docs/EDU-BRIDGE.md 契约 v0.1 已确认
[ ] bridge 服务可部署（Docker 或 systemd）PIN 端口/版本
[ ] Principal 入会话可证
[ ] ≥2 只读工具 + 跨校拒绝
[ ] 提案流无 Agent 直写
[ ] Ce0–Ce4、Ce6 PASS（Ce5 至少 1 条审）
[ ] 课件 G1 回归仍 PASS
[ ] RUNBOOK + Issue + PIN 回写
[ ] 未宣称 CLAIM-B（除非 E1 已过）
[ ] 未授权外的写库接口未暴露给 Agent
```

---

## 9. 风险

| 风险 | 缓解 |
|------|------|
| edu-core 接口不清 | C0 Mock 同契约 |
| Dify 难透传用户 JWT | bridge 换票端点 + 会话 cookie |
| 提示词诱导「已写入」 | 系统提示 + 无写工具 + Ce3 |
| 与 E1 后置叠加暴露 | bridge 仅内网/鉴权；不公开匿名 |
| 范围膨胀成全 SIS | 死守只读白名单 + 提案 |

---

## 10. 关联

| 文件 | 用途 |
|------|------|
| `docs/EDU-BRIDGE.md` | 契约 |
| `bridge/README.md` | 服务说明 |
| `ops/C-PATH-RUNBOOK.md` | 勾选 |
| `docs/ARCHITECTURE.md` | L7 |
| `ops/DEBT-LEDGER.md` | C 状态 |
