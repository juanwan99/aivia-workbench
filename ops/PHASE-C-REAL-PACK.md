# 阶段 C-REAL · 真身份 + 真只读 + Dify 可达

```
STATUS: BINDING · 业主点名下一能力线
DATE: 2026-08-06
CODE: PHASE-C-REAL
前提: CLAIM-C + CLAIM-C-FIX 绿(mock) · E1 后置 · CLAIM-B 仍否
出口: MODE=real 或 hybrid · 真/准真 IdP · 只读白名单打真数据 · Dify 工具可调 bridge · Ce 回归绿
对标: 一线租户/SSO/只读连接器 · 仍禁止 Agent 直写
```

> **≠ CLAIM-B。** 证书后置则对外仍「内测/知悉自签」。  
> **禁止** 为连通 Dify 把 bridge 绑公网 `0.0.0.0` 无鉴权。  
> **禁止** 重做 A/B 大包。

---

## 0. 要解决的产品问题

mock 已证：**契约能跑**。  
REAL 要证：**老师用真（或预发）学校身份进工作台，Agent 能查本校真只读数据，变更仍只提案。**

| 用户真相 | REAL 必须 |
|----------|-----------|
| 我是真校老师 | 真 IdP / edu 签发 token（或预发等价） |
| 班/课是真的 | 只读 API 打 edu-core 白名单 |
| 在 Chat 里能用 | Dify **容器网络**能调到 bridge |
| AI 不改成绩 | 仍无 apply；提案不直写 |

---

## 1. 对标（行为）

| 一线 | 本包 |
|------|------|
| SSO/OIDC | C-R1 接 edu IdP 或桥接换票 |
| 租户隔离 | path school_id == token |
| 连接器最小权限 | 只读白名单 2+ |
| 人审写 | 提案保留 |
| 网络零信任 | 内网/host gateway + 鉴权，不公网裸奔 |

---

## 2. 工作包（按序）

### C-R0 · 发现钉死（1 次 · 门）

必须书面（Issue + `docs/EDU-BRIDGE.md` 升 v0.2）：

| 项 | 内容 |
|----|------|
| edu-core 基址 | 内网 URL（无密钥进仓） |
| IdP | OIDC / JWT 签发方 / 密钥校验方式 |
| 只读白名单 | 最终 path 列表（classes/courses 等） |
| 禁止写 | grades 等仍禁止 |
| 网络 | Dify 容器 → bridge 路径选型（见 C-R2） |
| 环境 | 预发 / 生产只读账号 |

**若 edu 暂不可给真接口：** 允许 **hybrid**：IdP mock 闸门保留 + 只读打 **fixture 真结构 JSON 文件**（来自脱敏导出）——须 Issue 钉 `MODE=hybrid`，不得标 `real` 满绿。

### C-R1 · 真身份

| 交付 | 验收 |
|------|------|
| 校验 edu JWT 或 OIDC code→token | `/me` 含真实 school_id/role |
| 关掉「任意 role 自助 exchange」或仅内网 + 强 EXCHANGE_TOKEN | 外网/无 token 不能领 admin |
| exp/签名失败 401 | smoke 扩一条 |

### C-R2 · Dify ↔ bridge 网络（F2 还债）

**推荐顺序（择一钉死）：**

| 方案 | 做法 | 风险 |
|------|------|------|
| **A host-gateway** | Dify 工具 URL = `http://172.17.0.1:18090` 或 compose `extra_hosts: host.docker.internal`；bridge 仍 **127.0.0.1 或 docker0** | 仅 Docker 网可达 |
| **B 同网 bridge 容器** | bridge 进 compose 网络，名 `aivia-bridge:18090`；**不** publish 公网端口 | 佳 |
| **C 反代内网 path** | nginx 仅允许 Docker 网段访问 `/bridge` | 配错易暴露 |

**禁止：** `0.0.0.0:18090` 对公网 + 匿名 exchange。

验收：在 **api 容器内** `curl` bridge health 200。

### C-R3 · 只读真数据

- 实现 `MODE=real`（或 hybrid fixture）下 classes + course meta  
- 跨校仍 403  
- 下游 502 → 人话  

### C-R4 · Dify 工具挂载

- 导入/更新 openapi  
- 默认演示应用或课件应用挂：`list_my_classes`、`get_course_meta`、`create_proposal`  
- 鉴权：如何把用户 JWT 传给工具（Dify 配置 + 文档）  
- Chat 一轮：问「本校班级」→ 工具命中  

### C-R5 · 提案与审计不回退

- create_proposal / apply 403 / admin 审 仍绿  
- audit 有真实 sub/school  

### C-R6 · 回归金路径 Ce-R

| ID | 过线 |
|----|------|
| Ce-R0 | 真/hybrid Principal |
| Ce-R1 | G1 课件仍 DOWNLOAD_READY |
| Ce-R2 | 只读本校真数据（或 hybrid fixture） |
| Ce-R3 | 跨校 403 |
| Ce-R4 | 提案 pending |
| Ce-R5 | 人审一条 |
| Ce-R6 | Dify 内工具至少 1 次成功 |
| Ce-R7 | smoke.sh（扩展）PASS |

---

## 3. CLAIM-C-REAL

```text
[ ] C-R0 契约 v0.2 钉死 MODE=real|hybrid
[ ] C-R1 真身份校验
[ ] C-R2 容器内可达 bridge（非公网裸）
[ ] C-R3 只读白名单通
[ ] C-R4 Dify 工具挂载 + Chat 命中
[ ] C-R5 提案/无 apply
[ ] C-R6 Ce-R 全过
[ ] PIN + RUNBOOK + Issue
[ ] 未勾 CLAIM-B
```

**hybrid 只可报 CLAIM-C-REAL(hybrid)，不可报 full real。**

---

## 4. 风险

| 风险 | 缓解 |
|------|------|
| edu 接口延期 | hybrid fixture |
| 网络配错公网暴露 | 检查 ss；仅内网；exchange token 强制 |
| JWT 如何进 Dify 工具 | C-R4 专章；必要时 bridge 会话票 |
| 范围膨胀写库 | 死守白名单 |

## 5. 关联

`ops/C-REAL-RUNBOOK.md` · `docs/EDU-BRIDGE.md` · `bridge/` · `ops/PHASE-C-FIX-DEPLOY-PACK.md`
