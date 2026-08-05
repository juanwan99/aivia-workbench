# 阶段 D · PILOT-LITE 执行清单

日期：2026-08-06    执行人：phase-d-pilot-lite（ECS）  
工作台：`https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl`  
Dify pin：`1.16.1`    DeepSeek：`deepseek-chat`  
证书：自签（已知警告）    edu：不接 real    E1：不做  

正文：`ops/PHASE-D-PILOT-LITE-PACK.md`  
**进仓证据（真源）：** `ops/evidence/d-pilot-lite/`  
服务器镜像（非仓）：`/home/ops/aivia-phase-d-pilot-lite/`

## D0 开场

- [x] 入口可打开（证书警告：是 / 自签）  
- [x] passport + `/api/parameters` 200（loopback `127.0.0.1:13080`）  
- [x] 未关闭限流 / 未刷配额  
- **D0 结果：** **PASS**

## D1 会话记录（≥3）

| # | 场景 | conv_id | 要文件? | 产物（仓内） | DOWNLOAD_READY | 结果 | 备注 |
|---|------|---------|---------|--------------|----------------|------|------|
| S1 | HTML 一句话（细胞结构） | `09989ede-05de-4a06-9d14-35fa38595507` | 是 | `ops/evidence/d-pilot-lite/s1-t1-artifact.html` | 是 | **PASS** | ~24s · 可开有标题 |
| S2 | 同会话改稿（一元二次方程→求根公式例题） | `814f1190-b146-4258-a25f-ea6f7d304e2c` | 是 | `ops/evidence/d-pilot-lite/s2-t2-artifact.html` | 是 | **PASS** | 两轮均出件；同 passport |
| S3 | 教案 MD（《背影》） | `96aabf15-acb7-41e2-bdbf-7f278e91855f` | 是 | `ops/evidence/d-pilot-lite/s3-t1-artifact.md` | 是 | **PASS** | 非 Word |
| S4 | 只要大纲（光合作用） | `aff26289-1646-4b70-9d7c-a50cf149f372` | 否 | `ops/evidence/d-pilot-lite/s4-t1-answer.head.txt` | 否 | **PASS** | 无假 DOWNLOAD_READY |

空成功次数（要文件）：**0**  
会话数：**4**（≥3）  
质量抽检：S1/S2 HTML 可开+有标题；S3 md 结构完整  
计分 meta：`ops/evidence/d-pilot-lite/pilot-meta.json`

## D2 轻运维（可选）

- [x] bridge `/health`：`ok` · mode=mock · version=0.1.1 · loopback only  
- [x] 异常备注：首轮 S2-t2 因**每轮换 passport** 导致 404（会话归属 end_user）；**同 passport 重跑 PASS**（产品浏览器会话无此问题）  

## D3 交付（硬门禁）

- [x] RUNBOOK 本文件填满  
- [x] `ops/evidence/d-pilot-lite/` 真文件进仓  
- [x] `ops/evidence/d-pilot-lite/pilot-meta.json`  
- [x] 短报告 `ops/D-PILOT-LITE-REPORT.md`  
- [x] CANON / HANDOFF / README / PIN / PROJECT-PLAN 回写（无密钥）  
- [x] Issue #1 执行回写评论（无密钥）  
- [x] push `main`  

## CLAIM-D-LITE

- [x] ≥3 会话 + 空成功 0 + 短报告 + 下一刀  
- [x] 真文件进仓（非仅服务器本地）  
- [x] **未**勾 CLAIM-B  
- [x] **未**做全校推广 / 关限流 / E1 / edu real  

```text
摘要：
日期: 2026-08-06
会话数: 4
空成功: 0
CLAIM-D-LITE: YES
CLAIM-B: NO
正式上线: 否
进仓证据: ops/evidence/d-pilot-lite/
备注: 试点完成 ≠ 正式上线 · 自签已知
```
