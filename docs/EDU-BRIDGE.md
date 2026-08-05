# edu 身份桥 · 契约 v0.2

```
STATUS: BINDING · 阶段 C-REAL
MODE: hybrid（2026-08-06）
UPDATED: 2026-08-06
BINDING 约束: AI 不直写 edu 业务库
```

## 1. 目标

把 **学校租户 + 成员角色** 安全注入 Aivia Workbench（Dify），并提供 **只读查询** 与 **变更提案**。  
v0.2 在 v0.1 mock 之上钉死 **hybrid / real** 分层，禁止把 fixture 说成 live full real。

## 2. MODE

| 值 | 含义 | 可报 CLAIM |
|----|------|------------|
| `mock` | 内存假数据 | CLAIM-C（历史） |
| **`hybrid`（现行）** | 换票闸门 + **fixture 真结构 JSON**；edu-core 业务只读 API 未就绪 | **CLAIM-C-REAL(hybrid)** |
| `real` | 真 IdP 校验 + edu-core 只读白名单 live | CLAIM-C-REAL full（后置） |

## 3. Principal（JWT claims 最小集）

| claim | 类型 | 必填 | 说明 |
|-------|------|------|------|
| `sub` | string | 是 | 用户稳定 ID |
| `school_id` | string | 是 | 租户 |
| `role` | string | 是 | `teacher` \| `school_admin` \| `staff` |
| `name` | string | 否 | 展示名 |
| `exp` | number | 是 | 过期 |
| `iss` | string | 是 | `bridge-mock` / **`bridge-hybrid`** / `bridge-real` |

## 4. bridge HTTP

基路径：`/bridge/v1`

| 部署视角 | URL（示例） |
|----------|-------------|
| 主机运维 | `http://127.0.0.1:18090/bridge/v1` |
| Dify 容器 | `http://aivia-bridge:18090/bridge/v1` 或容器 IP |

| 方法 | 路径 | 鉴权 | 说明 |
|------|------|------|------|
| POST | `/auth/exchange` | **X-Bridge-Exchange-Token**（hybrid 强制） | 换 bridge JWT（非公开匿名） |
| GET | `/me` | Bearer | 当前 Principal |
| GET | `/schools/{school_id}/classes` | Bearer | 只读班级；path school == token |
| GET | `/schools/{school_id}/courses/{id}` | Bearer | 只读课程元数据 |
| POST | `/proposals` | Bearer | 创建提案 |
| GET | `/proposals` | Bearer | 列表（本校） |
| POST | `/proposals/{id}/review` | Bearer + school_admin | 人审 |
| GET | `/audit` | Bearer + school_admin | 审计（脱敏） |
| GET | `/health` | 无 | 健康检查 |

**不提供** 给 Agent：`PUT /grades`、任意 edu 写接口代理、`/proposals/{id}/apply`。

## 5. 只读白名单 / 禁止写

**只读（Agent 可调）：** classes 列表、course 元数据。  

**hybrid 数据源：** `bridge/data/hybrid-fixture.json`（脱敏结构样例）。  
**real 数据源（后置）：** edu-core 白名单 HTTP；现行 BFF 仅 `/health` 可探。  

**禁止 Agent：** 成绩写、学籍写、排课写、任意 `apply` 提案。

## 6. 网络（C-R2）

| 方案 | 现行 |
|------|------|
| B 同网容器 | **已用**：`aivia-bridge` ∈ `dify_default` |
| SSRF | 允许 `aivia-bridge` 域名 + bridge 容器 IP（仅运维 `.env`，无密钥） |
| 禁止 | 公网匿名 `0.0.0.0:18090` 无 exchange token |

## 7. 提案 payload 示例

```json
{
  "type": "lesson_plan_archive",
  "title": "豌豆杂交教案归档",
  "ref": { "artifact_name": "v6-artifact.md" },
  "note": "请教务归档"
}
```

## 8. 错误

| HTTP | 含义 |
|------|------|
| 401 | 无/过期 token / 坏 exchange token |
| 403 | 跨校或角色不足 / apply |
| 404 | 资源不存在 |
| 501 | MODE=real 未实现路径 |
| 502 | edu 下游失败（人话给 Dify） |

## 9. C0 / C-REAL 确认栏

- [x] 只读白名单：classes + course meta  
- [x] 禁止写：grades / apply  
- [x] **MODE=hybrid** 钉死（edu 业务只读未就绪）  
- [x] 日期：2026-08-06 · Issue #1  
