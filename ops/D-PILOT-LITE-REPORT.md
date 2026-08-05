# PHASE-D-PILOT-LITE 短报告

```
DATE: 2026-08-06
入口: https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl
CLAIM-D-LITE: YES
CLAIM-B: NO
正式上线: 否
```

## 1. 结论（一句话）

默认课件入口在 **自签 / 内测** 条件下，**4/4 会话产品路径可用**（HTML 出件、同会话改稿、教案 MD、大纲不假绿），**空成功 0**；  
**可报轻量内测完成，不可报教师正式上线。**

## 2. 会话证据

| 会话 | 结果 | 耗时量级 | 产物 |
|------|------|----------|------|
| S1 HTML 课件 | PASS | ~24s | `s1-t1-artifact.html` + DOWNLOAD_READY |
| S2 改稿 | PASS | ~24s + ~28s | `s2-t2-artifact.html` + DOWNLOAD_READY |
| S3 教案 MD | PASS | ~20s | `s3-t1-artifact.md` + DOWNLOAD_READY |
| S4 只要大纲 | PASS | ~3s | 无文件 · 无 DOWNLOAD_READY |

- **进仓证据：** `ops/evidence/d-pilot-lite/`（`pilot-meta.json` + 样例产物）  
- 勾选：`ops/D-PILOT-RUNBOOK.md`  
- 服务器镜像（非仓）：`/home/ops/aivia-phase-d-pilot-lite/`  
- 限流：**未关闭**（符合「禁刷数」）

## 3. 产品/运营观察

| 观察 | 说明 |
|------|------|
| 出件形态 | 现网仍为 **data-URL + DOWNLOAD_READY**（与 Harden/DEBT 一致） |
| 改稿 | 同会话第二轮可再导出完整 HTML |
| 教案 | v0.x = **Markdown only**（非 Word） |
| 证书 | 浏览器自签警告 **仍在**；内测需先点继续 |
| edu | **未接**；bridge mock 健康，本窗不测 Ce 全套 |
| API 内测注意 | 脚本若每轮新 passport，续聊会 404；**浏览器用户会话无此坑** |

## 4. 风险（低）

1. **E1 未做** → 外网教师信任/无警告打开仍阻断 CLAIM-B  
2. **全校未授权** → 禁止推广话术与扩人  
3. **账单级日配额** 仍可后置；现有并发/频控保持  

## 5. 下一刀建议（择一 · 业主拍板）

| 优先级 | 刀 | 解锁什么 | 本窗 |
|--------|----|----------|------|
| **P0** | **E1 DNS-01**（或云厂商证书） | 浏览器无警告 → 才谈 CLAIM-B / M5 扩教师 | 未做（任务禁 E1） |
| P1 | **PHASE-C-REAL** | edu-core 只读白名单接真 · 回归 Ce2–Ce5 | 未做（不接 edu） |
| P2 | Dify 控制台挂载 bridge OpenAPI | 工作台内可点只读工具（增强，非门禁） | 书面后置可续 |
| — | 全校推广 / 关限流 | **禁止** | — |

**推荐默认下一刀：** 业主侧推进 **E1 DNS-01**；应用侧保持现状可内测，**不要**用 CLAIM-D-LITE 换 CLAIM-B 叙事。

## 6. 口径备忘

```text
CLAIM-D-LITE = 轻量内测会话完成
≠ 正式上线
≠ CLAIM-B
≠ M5 全量教师试点
```
