# 阶段 C · edu 桥执行清单

日期：2026-08-05    执行人：phase-c-run（ECS）  
MODE： **mock**  
工作台：`https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl`  
bridge 基址：`http://127.0.0.1:18090/bridge/v1`  
版本：`0.1.0`  

正文：`ops/PHASE-C-PACK.md` · 契约：`docs/EDU-BRIDGE.md`

## C0 契约

- [x] edu-core 形态已记录（BFF health 可探；业务 OIDC/只读 API 未挂 → **Mock 同契约**）  
- [x] 只读白名单：classes + course meta  
- [x] 禁止写列表：grades / apply / 任意 edu 写代理  
- [x] EDU-BRIDGE.md v0.1  
- **结果：** **PASS**（MODE=mock 钉死）  

## C1 身份

- [x] JWT/Principal 含 school_id + role（`/auth/exchange` → `/me`）  
- [x] exp 失效 401  
- **结果：** **PASS**  

## C2 注入

- [x] 工具/调用带身份（Bearer Principal）  
- [x] 角色边界：teacher 可提案不可审；school_admin 可审  
- [x] OpenAPI 描述：`bridge/openapi.json`（供 Dify 自定义工具）  
- **结果：** **PASS**  

## C3 只读

- [x] 工具1：`list_my_classes` → `/schools/{id}/classes`  
- [x] 工具2：`get_course_meta` → `/schools/{id}/courses/{cid}`  
- [x] 跨校 403；无 token 401  
- **结果：** **PASS**  

## C4 提案

- [x] create_proposal → pending_review  
- [x] Agent 无 apply（`/proposals/{id}/apply` → 403）  
- [x] 人审路径：`/proposals/{id}/review`（admin）  
- **结果：** **PASS**  

## C5 审计

- [x] `/audit` 可查（admin）  
- [x] 无密钥进日志  
- **结果：** **PASS**  

## Ce 金路径

| ID | 结果 | 备注 |
|----|------|------|
| Ce0 有 Principal | **PASS** | teacher-demo / school-demo |
| Ce1 课件仍可下载 | **PASS** | G1 回归 DOWNLOAD_READY · `g1-regression.html` |
| Ce2 只读本校 | **PASS** | classes + bio-pea |
| Ce3 跨校/无 token 失败 | **PASS** | 403 / 401 人话 |
| Ce4 提案 pending | **PASS** | 创建 pending；无业务直写 |
| Ce5 人审 | **PASS** | 拒绝 1 条 + 通过 1 条 |
| Ce6 审计 | **PASS** | audit.jsonl 脱敏 |

空成功（出件+桥）：**0**  

产物目录：`/home/ops/aivia-phase-c-artifacts/`

## CLAIM-C

- [x] 可报阶段 C 绿（PACK §8 · MODE=mock）  
- [x] **未**勾 CLAIM-B（E1 后置）  

```text
摘要：MODE=mock · Ce 全 PASS · school-demo · bridge 0.1.0 · 127.0.0.1:18090
CLAIM-C: YES (mock)
CLAIM-B: NO (E1 deferred)
```
