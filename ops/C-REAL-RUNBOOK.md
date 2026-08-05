# C-REAL 勾选清单

日期：2026-08-06    MODE： **hybrid**（非 full real）  
bridge 基址（Dify 视角）：`http://aivia-bridge:18090/bridge/v1`（容器）· 工具实测 IP `172.22.0.15:18090`  
edu 基址（脱敏）：`http://127.0.0.1:8080` edu-core-bff **仅 /health** · 业务只读 API **未挂**  
执行人：phase-c-real-hybrid  

正文：`ops/PHASE-C-REAL-PACK.md` · 契约：`docs/EDU-BRIDGE.md` v0.2  

## C-R0

- [x] 契约 v0.2 / Issue 钉白名单与 IdP  
- [x] MODE=**hybrid**（fixture 真结构；非 live edu 查询）  
- **结果：** **PASS（hybrid 钉死）**  

## C-R1 身份

- [x] hybrid 换票 → `/me` 含 school_id/role（iss=`bridge-hybrid`）  
- [x] 强制 EXCHANGE_TOKEN；坏 token 401  
- [x] exp 失效 401  
- **结果：** **PASS（hybrid 闸门）**  

## C-R2 网络

- [x] 方案 **B**：`aivia-bridge` 容器加入 `dify_default`  
- [x] 容器内 health 200（dify-api → aivia-bridge）  
- [x] 主机 process 仍可 `127.0.0.1:18090` 运维/smoke  
- [x] 非公网匿名 exchange（token 强制）  
- [x] SSRF：`SSRF_PROXY_ALLOW_PRIVATE_DOMAINS=aivia-bridge` + `SSRF_PROXY_ALLOW_PRIVATE_IPS=<bridge_ip>`  
- **结果：** **PASS**  

## C-R3 只读

- [x] classes（fixture · source=hybrid-fixture）  
- [x] course meta  
- [x] 跨校 403  
- **结果：** **PASS（fixture）**  

## C-R4 Dify

- [x] 工具已挂 应用/空间：provider `aivia_edu_bridge`（OpenAPI）  
- [x] Chat/控制台工具命中：`list_my_classes` test/pre **PASS**（3 班 fixture）  
- **结果：** **PASS**（证据 `ops/evidence/c-real-hybrid/tool-test-list-classes.json`）  

## C-R5 提案

- [x] pending / apply 403 / 人审  
- **结果：** **PASS**（smoke）  

## Ce-R

| ID | 结果 | 备注 |
|----|------|------|
| Ce-R0 | **PASS** | hybrid Principal |
| Ce-R1 G1 | **PASS** | DOWNLOAD_READY · `ce-r1-g1-head.txt` |
| Ce-R2 只读 | **PASS** | fixture classes |
| Ce-R3 跨校 | **PASS** | 403 |
| Ce-R4 提案 | **PASS** | pending |
| Ce-R5 人审 | **PASS** | admin reject |
| Ce-R6 Dify 工具 | **PASS** | list_my_classes |
| Ce-R7 smoke | **PASS** | 13/13 |

## CLAIM

- [x] **CLAIM-C-REAL(hybrid)**  
- [ ] CLAIM-C-REAL full（live edu API）— **未**  
- [x] **未** CLAIM-B  
- [x] PIN MODE=hybrid · EDU-BRIDGE v0.2 · Issue 摘要  

```text
CLAIM-C-REAL(hybrid): YES
CLAIM-C-REAL full: NO (edu only-read API not ready; BFF /health only)
CLAIM-B: NO
MODE: hybrid
bridge: 0.2.0 · aivia-bridge container + host smoke
```
