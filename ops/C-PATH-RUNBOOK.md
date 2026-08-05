# 阶段 C · edu 桥执行清单

日期：________    执行人：________  
MODE： mock / real-edu（圈一）  
工作台：`https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl`  
bridge 基址：________  

正文：`ops/PHASE-C-PACK.md` · 契约：`docs/EDU-BRIDGE.md`

## C0 契约

- [ ] edu-core 形态已记录（或 Mock）  
- [ ] 只读白名单  
- [ ] 禁止写列表  
- [ ] EDU-BRIDGE.md v0.1  
- **结果：** PASS / FAIL  

## C1 身份

- [ ] JWT/Principal 含 school_id + role  
- [ ] exp 失效 401  
- **结果：** PASS / FAIL  

## C2 注入

- [ ] 工具调用带身份  
- [ ] 角色边界  
- **结果：** PASS / FAIL  

## C3 只读

- [ ] 工具1：________  
- [ ] 工具2：________  
- [ ] 跨校 403  
- **结果：** PASS / FAIL  

## C4 提案

- [ ] create_proposal → pending  
- [ ] Agent 无 apply  
- [ ] 人审路径存在  
- **结果：** PASS / FAIL  

## C5 审计

- [ ] 日志可查  
- [ ] 无密钥进日志  
- **结果：** PASS / FAIL  

## Ce 金路径

| ID | 结果 | 备注 |
|----|------|------|
| Ce0 有 Principal | | |
| Ce1 课件仍可下载 | | |
| Ce2 只读本校 | | |
| Ce3 跨校/无 token 失败 | | |
| Ce4 提案 pending | | |
| Ce5 人审 | | |
| Ce6 审计 | | |

空成功（出件+桥）：____  

## CLAIM-C

- [ ] 可报阶段 C 绿（PACK §8）  
- [ ] 未勾 CLAIM-B（E1 未过则禁止）  

```text
摘要：MODE / Ce / school 测试 id / bridge 版本 / 备注
```
