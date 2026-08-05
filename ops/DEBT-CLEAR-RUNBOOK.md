# 阶段 DEBT-CLEAR 勾选清单

日期：2026-08-05    执行人：phase-debt-clear（ECS）  
默认入口：`https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl`  
Dify：`1.16.1`    DeepSeek：`deepseek-chat`  

正文：`ops/PHASE-DEBT-CLEAR-PACK.md`

## E0 真源

- [x] PACK + 本 RUNBOOK 落盘  
- [x] CANON / HANDOFF / README / PIN / INFRA 同步  
- [x] Issue #1 回写（本窗）  
- **结果：** PASS  

## E1 证书公网（P0）

- [ ] 浏览器无证书警告  
- [x] 公网 HTTPS 可打开默认 Chat（自签警告下 200；非站点 403）  
- [x] HTTP-01 实测：外网 LE 校验 **403 / 空 body**（本机 webroot 有 body）  
- [ ] DNS-01 或云证书安装 + reload  
- **结果：** **BLOCKED** · 需阿里云 DNS API/手工 TXT 或平台证书  
- **解锁：**  
  1. 业主在阿里云 DNS 为 `_acme-challenge.workbench` 添加 TXT（certbot DNS-01 给出值）  
  2. 或提供仅 DNS 编辑权限的 RAM AK（勿进 Git）后 `acme.sh --dns dns_ali`  
  3. `systemctl reload nginx`（经 systemd；勿裸 `nginx -s stop`）  

## E2 日配额

- [x] 并发 `max_active_requests=8`  
- [x] nginx `limit_req 30r/m/IP`（burst 20）+ 429 人话 JSON  
- [x] 超时 `proxy_read_timeout 3600s`  
- [x] **账单级日 token 后置书面**（社区版无原生日消息账单开关）  
- **结果：** PASS（等价试点；账单级后置）  

## E3 附件 / 大文件

- [x] 正式形态：**data-URL 一键下载**（Code 节点 DOWNLOAD_READY）  
- [x] 非「仅长代码请自行保存」  
- [x] 大文件策略：`client_max_body_size 100M`；课件建议 &lt;2MB / 过大拆分  
- [ ] Dify storage 附件升档（后置）  
- **结果：** PASS（data-URL 正式；storage 后置）  

## E4 教案

- [x] 永久 scope = **MD only**（skills 已名实）  
- [ ] DOCX（后置）  
- **结果：** PASS（永久 MD）  

## E5 知识库

- [x] `Aivia课件结构模板` · economy  
- [x] 无 embedding 前 economy 为永久口径  
- **结果：** PASS  

## E6 证据

- [x] 抽检：`v1/v5/v8` HTML + `v6` 教案 MD（`/home/ops/aivia-phase-debt-clear/`）  
- [x] 另有 harden `r1/r2` HTML + phase-b `t4` 教案  
- **结果：** PASS  

## E7 运维

- [x] 磁盘：约 **84%** 使用 / 约 31G 可用（告警）  
- [x] Pico `https://pico.aivia.asia` **200**  
- [x] 备份脚本存在；未改 Pico 域名  
- [x] 事故：E1 尝试中曾停 nginx · 已 `systemctl start nginx` 恢复  
- **结果：** PASS（磁盘告警记 Issue）  

## E8 回归 V1–V8

| # | 结果 | 产物 / 备注 |
|---|------|-------------|
| V1 | **PASS** | v1-artifact.html · DOWNLOAD_READY |
| V2 | **PASS** | v2-artifact.html · DOWNLOAD_READY |
| V3 | **PASS** | 大纲无假文件 |
| V4 | **PASS** | 明确失败人话 |
| V5 | **PASS** | v5-artifact.html · DOWNLOAD_READY |
| V6 | **PASS** | v6-artifact.md · DOWNLOAD_READY |
| V7 | **PASS** | v7-artifact.md · DOWNLOAD_READY |
| V8 | **PASS** | v8-artifact.html · DOWNLOAD_READY |

空成功：**0**

## CLAIM

| 层 | 状态 |
|----|------|
| CLAIM-A 债务清零 | **NO**（E1 未满） |
| CLAIM-B 教师正式可用 | **NO**（E1 未满） |
| 应用侧 E2–E7 + E8 | **YES** |

```text
摘要：
日期: 2026-08-05
空成功: 0
E1: BLOCKED (HTTP-01 外网 403/空 body → 需 DNS-01)
E2: PASS (max_active_requests=8 + nginx 30r/m；日 token 后置)
E3: PASS (data-URL 正式；storage 后置)
E4: PASS (MD only 永久)
E5: PASS (economy 永久)
E6: PASS
E7: PASS (Pico 200；磁盘 84%)
E8: PASS 空成功 0
CLAIM-A: NO
CLAIM-B: NO
备注: 应用侧可内测；禁止教师正式上线直至 E1
```
