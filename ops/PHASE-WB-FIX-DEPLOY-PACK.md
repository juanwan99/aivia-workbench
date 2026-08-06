# 任务包 · WB-FIX-DEPLOY（ALIGN 后修复 + 现网部署）

```
STATUS: DONE · CLAIM-WB-FIX-DEPLOY=YES · 正式上线=否
DATE: 2026-08-06
CODE: PHASE-WB-FIX-DEPLOY
前提: CLAIM-WB-ALIGN=YES（有条件）· 正式上线=否
执行窗: 本机 Grok + SSH 云端 + 本机浏览器/Office
目的: 消化深度审查残留 · 把「等价偏弱」做硬 · 部署到现网可演示 · 再回归
产出: evidence/wb-fix-deploy · NOTES · REPORT · workflow=fix-deploy
```

> **不是重开全量对标。** 范围 = 审查点名的修复 + 现网部署验收。  
> **模式：** F0→F4 串行；每阶段 gate 自审；FAIL 则修；禁止跳阶段假绿。  
> **禁止：** 空成功、data-URL 主路径、`[blocked]`、密钥进仓、Agent 写库、假 1:1、未授权全校上线。

---

## 0. 审查残留清单（本包必消化）

| ID | 残留 | 本包目标 |
|----|------|----------|
| R1 | C-01/A-07 仅「文本材料」顶替上传 | **真文件上传再加工** 至少 1 条可演示（Dify 文件变量或等价前台控件） |
| R2 | B-09 仅聊天链清单 | **稳定下载区**：回答内固定「交付清单」模板（多文件多行 https `/dl`）+ 截图/文本证据 |
| R3 | DOCX 偶发 md / 弱扩展名 | **扩展名/MIME 门禁**：非 docx/xlsx/html/md 策略明确；DOCX 连续 2 次 PASS |
| R4 | S7 弱指令仍可能带文件 | 默认系统提示强化「只要大纲严禁 DOWNLOAD」；弱指令抽测 PASS |
| R5 | 公网 TLS 边缘不稳 | 记录+尽量缓解（nginx/证书链/HSTS 不破坏）；**至少源站与 1 条外网路径** 写清 |
| R6 | 管理 ops 仅容器内可知 | **部署说明 + 现网烟测**：metrics/audit/policy 在部署后可调（token 不进仓） |
| R7 | DEBT/真源滞后 | DEBT 关 ALIGN；FIX 状态进 PIN/CANON |
| R8 | bridge 0.2.2 需确认现网 | 容器/进程版本与健康检查进证据 |

**明确不在本包：** 专家目录完整 UI、edu full real、桌面/IM、正式上线运营。

---

## 1. 整包完成定义 CLAIM-WB-FIX-DEPLOY

```text
[ ] F0–F4 gate 全 PASS
[ ] R1–R8 均有处置（有/缓解+说明），无静默忽略
[ ] 用户：HTML + XLSX + DOCX 各 1 · /dl · 无 blocked · 本机打开
[ ] 上传再加工 1 次真文件路径 PASS
[ ] 大纲弱指令无假 DOWNLOAD
[ ] 管理：现网 /ops/metrics 与 policy 烟测证据（脱敏）
[ ] 部署记录 ops/WB-FIX-DEPLOY-NOTES.md（改了什么、怎么重启、如何回滚）
[ ] 回归空成功 0
[ ] PIN/CANON/HANDOFF/DEBT + Issue + push
[ ] 正式上线仍否
```

---

## 2. 无人值守协议

```text
for stage in F0..F4:
  执行 → 写 gate-F{n}.md 自审
  FAIL → 修复循环 → 重审
  仍 FAIL → 整包 BLOCKED，停
  PASS → 自动下阶段
终：REPORT + 回写
```

证据根：`ops/evidence/wb-fix-deploy/`

---

## 3. 阶段

### F0 · 现网基线冻结

| 做 | 过线 |
|----|------|
| 记录 bridge 版本、容器状态、Dify Chat 入口 | `F0/baseline.md` |
| 抽 `/dl` 与拒写库 | 绿 |
| 确认密钥仅 secrets | 无仓内 secret |

### F1 · 交付与格式加固（R2/R3/R4）

| 做 | 过线 |
|----|------|
| PackDownload/提示词：交付清单模板（多行 `/dl`） | 样例 answer 含清单 |
| DOCX 强制：连续 2 次要 Word 得 `.docx` `/dl` | 2 artifacts OOXML |
| 大纲：弱指令「列要点就行」无 DOWNLOAD | PASS |
| 禁止 data-URL 主路径回潮 | 扫描 PASS |

### F2 · 上传再加工（R1）

| 做 | 过线 |
|----|------|
| Dify 启用文件输入或工作流读用户文件 | 配置可指 |
| 本机或 API：**上传/附带一文件** → 生成可下载产物 | evidence 含源说明+产物 |
| 若平台限制：给出 **最小可用** 路径（如 Chat 文件按钮）截图/步骤 | 步骤可复现 |

### F3 · 部署管理面 + TLS 说明（R5/R6/R8）

| 做 | 过线 |
|----|------|
| 现网 bridge 0.2.2+ 部署/确认 restart | health 含 version |
| `/ops/metrics` `/ops/policy` 烟测（token 脱敏） | json 进 evidence |
| TLS：openssl/curl 源站结果 + 已知边缘问题写入 NOTES | 不装没事 |
| 回滚：上一镜像/compose 要点 | NOTES 有回滚节 |

### F4 · 全回归 + 真源 + 收口

| 做 | 过线 |
|----|------|
| 三格式 + 大纲 + 拒写 + 上传链 再跑 | 空成功 0 |
| DEBT 关 ALIGN 开 FIX 关或转下项 | 一致 |
| `WB-FIX-DEPLOY-REPORT.md` | 结论+限制 |
| PIN `CLAIM-WB-FIX-DEPLOY=YES` | |

---

## 4. 自审模板

同 ALIGN：每阶段 `gate-F{n}.md` 含清单/FAIL 修复/空成功/密钥。

---

## 5. 关联

- 卡：`ops/TASK-CARD-WB-FIX-DEPLOY.md`  
- 勾选：`ops/WB-FIX-DEPLOY-RUNBOOK.md`  
- 上游审查结论：WB-ALIGN 深度审查残留  
