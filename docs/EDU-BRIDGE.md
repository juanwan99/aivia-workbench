# edu 身份桥 · 契约 v0.1

```
STATUS: CONFIRMED · 阶段 C · MODE=mock（C0 钉死 2026-08-05）
UPDATED: 2026-08-05
BINDING 约束: AI 不直写 edu 业务库
```

## 1. 目标

把 **学校租户 + 成员角色** 安全注入 Aivia Workbench（Dify），并提供 **只读查询** 与 **变更提案**，对标一线平台的组织边界与人机审批，而非匿名 Agent。

## 2. Principal（JWT claims 最小集）

| claim | 类型 | 必填 | 说明 |
|-------|------|------|------|
| `sub` | string | 是 | 用户稳定 ID |
| `school_id` | string | 是 | 租户 |
| `role` | string | 是 | `teacher` \| `school_admin` \| `staff` |
| `name` | string | 否 | 展示名 |
| `exp` | number | 是 | 过期 |
| `iss` | string | 是 | `bridge-mock` 或 edu |

## 3. bridge HTTP

基路径：`/bridge/v1`（本机默认 `http://127.0.0.1:18090`；经反代时勿裸奔无鉴权）

| 方法 | 路径 | 鉴权 | 说明 |
|------|------|------|------|
| POST | `/auth/exchange` | mock 凭据 | 换 bridge JWT |
| GET | `/me` | Bearer | 当前 Principal |
| GET | `/schools/{school_id}/classes` | Bearer | 只读班级；**path 与 token school 必须一致** |
| GET | `/schools/{school_id}/courses/{id}` | Bearer | 只读课程元数据 |
| POST | `/proposals` | Bearer | 创建提案 |
| GET | `/proposals` | Bearer | 列表（本校） |
| POST | `/proposals/{id}/review` | Bearer + school_admin | 人审 |
| GET | `/audit` | Bearer + school_admin | 审计（脱敏） |
| GET | `/health` | 无 | 健康检查 |

**不提供** 给 Agent：`PUT /grades`、任意 edu 写接口代理、`/proposals/{id}/apply`。

## 4. 提案 payload 示例

```json
{
  "type": "lesson_plan_archive",
  "title": "豌豆杂交教案归档",
  "ref": { "artifact_name": "v6-artifact.md" },
  "note": "请教务归档"
}
```

## 5. 错误

| HTTP | 含义 |
|------|------|
| 401 | 无/过期 token |
| 403 | 跨校或角色不足 |
| 404 | 资源不存在 |
| 502 | edu 下游失败（人话给 Dify） |

## 6. MODE

| 值 | 含义 |
|----|------|
| **`mock`（现行）** | 内存假数据，同契约；C0 已钉 |
| `real` | 调 edu-core 只读白名单（后置） |

## 7. 只读白名单 / 禁止写

**只读（Agent 可调）：** classes 列表、course 元数据。  

**禁止 Agent：** 成绩写、学籍写、排课写、任意 `apply` 提案。

## 8. C0 确认栏

- [x] 只读白名单：classes + course meta  
- [x] 禁止写列表：grades / roster write / apply  
- [x] **MODE=mock**（edu-core BFF 健康可探，OIDC/只读业务 API 未对接 → Mock 同契约）  
- [x] 日期：2026-08-05 · Issue #1  
