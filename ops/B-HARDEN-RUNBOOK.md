# 阶段 B 硬化清单（修复 · 优化 · 收尾）

日期：2026-08-05    执行人：phase-b-harden（ECS）  
默认入口：`https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl`  
Dify：`1.16.1`    DeepSeek：`deepseek-chat`  

正文：`ops/PHASE-B-HARDEN-PACK.md` · 收口：`ops/PHASE-B-CLOSEOUT.md`

## H0 真源

- [x] HANDOFF/CANON/README/PLAN 已指向 Harden 而非重做 B  
- [x] PIN B3 升格说明 + Harden 出口  
- **结果：** PASS  

## H1 真下载

- [x] 出件路径：Chatflow **Code 节点**打包 → `DOWNLOAD_READY` + **data-URL 点击下载**（控件）+ 源码备用  
- [x] 非「仅长代码请自行保存」  
- [x] R1 豌豆杂交  
- [x] R2 改稿仍有文件  
- 产物名：`r1-artifact.html` / `r2-artifact.html`  
- **结果：** PASS  

## H2 入口

- [ ] 证书无警告  
- [x] 公网可打开默认 Chat（自签警告下可继续访问）  
- [x] Issue「入口硬化」书面范围：**仅内网/知悉自签警告**（LE HTTP-01 仍 403，待 DNS-01）  
- **结果：** 范围限制：自签证书 · 未正式无警告  

## H3 真配额

- [x] 日限额或等价数字：应用 `max_active_requests=8`；nginx `limit_req` **30r/m/IP**（burst 20）  
- [x] 超时配置：nginx `proxy_read_timeout 3600s`；LLM `max_tokens=8192`  
- [x] 超限/失败人话验证：G4/R4 明确失败人话；站点 disclaimer 写明并发/额度策略  
- **结果：** PASS（试点起点；日 token 账单级配额可后置）  

## H4 教案

- [ ] DOCX 可下载  
- [x] 书面 scope=**MD only**（v0.x；DOCX 后置）  
- **结果：** PASS（缩 scope 诚实）  

## H5 单入口

- [x] 主推链唯一：`/chat/lOMVPbz7rZmbJSJl`  
- [x] 旧 Agent `enable_site=false`（公开下架）  
- **结果：** PASS  

## H6 抽检

- [x] 2 HTML + 1 教案记录进 Issue（r1/r2 HTML + 既有 t4 教案 MD）  
- **结果：** PASS  

## H7 回归五次

| # | 结果 | 产物 |
|---|------|------|
| R1 | PASS | r1-artifact.html + DOWNLOAD_READY |
| R2 | PASS | r2-artifact.html + DOWNLOAD_READY |
| R3 | PASS | 大纲无假文件 |
| R4 | PASS | 明确失败 |
| R5 | PASS | r5-artifact.html + DOWNLOAD_READY |

空成功：**0**

## 回写

- [x] Issue #1 Harden 结果  
- [x] PIN / CLOSEOUT 残留更新  
- [x] 未宣称 C/教师正式上线（H2 未满）  

```text
摘要：
日期: 2026-08-05
空成功: 0
H1形态: Code节点 data-URL 一键下载
证书: 自签（H2 范围限制）
配额: max_active_requests=8 + nginx 30r/m/IP
备注: 应用硬化绿；对外正式上线仍待 H2 正式证书
```
