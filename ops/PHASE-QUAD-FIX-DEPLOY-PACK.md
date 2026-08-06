# 任务包 · QUAD-FIX-DEPLOY（上线后修复+部署）

```
STATUS: BINDING · 单包单卡 · 无人值守自审
DATE: 2026-08-06
CODE: PHASE-QUAD-FIX-DEPLOY
调查: ops/QUAD-FIX-SURVEY.md
执行窗: 本机 Grok + SSH 云端（ECS + 边缘 dmit）+ 浏览器
```

> 消化 QUAD-LAUNCH 深度审查残留。**先修阻断体验，再加固运维，再补齐文档。**  
> 模式：X0→X4 串行 · gate 自审 · FAIL 则修 · 禁止跳阶段假绿。  
> 正式上线保持 **是（受限）**；FULL-REAL 保持 **NO**；禁止扩大为全校话术。

---

## 0. CLAIM-QUAD-FIX-DEPLOY

```text
[ ] X0–X4 gate 全 PASS
[ ] F1：curl -sI https://asyncova.com/experts 与 .../experts/ 均最终 200 专家页，Location 永不含 :8443
[ ] F2：隧道/反代有 systemd（或等价）unit + 探活说明；重启后专家+Chat 仍 200
[ ] F3：ops/experts/catalog.yaml 与 catalog 一致；QUAD-FIX-DEPLOY-NOTES 含部署/回滚
[ ] 回归：Chat 金路径 1 次 /dl；专家台点 1 卡出件或深链可用
[ ] 空成功 0 · 无密钥进仓
[ ] REPORT + PIN/CANON/DEBT + Issue + push
[ ] 正式上线仍=是（受限）· FULL-REAL=NO
```

---

## 1. 阶段

### X0 · 基线复现

| 做 | 过线 |
|----|------|
| 复现 experts 无 `/` 的 302 目标 | 截 header 进 evidence（证明修前问题） |
| Chat /experts/ 当前 200 | 记录 |
| 隧道进程现状 | 记录 pid/命令 |

`gate-X0.md`

### X1 · 修 F1 专家入口（P0）

| 做 | 过线 |
|----|------|
| 修边缘（及源站若同样）nginx：`/experts` 与 `/experts/` | **都不** rewrite 到 :8443 |
| 推荐：`location = /experts { return 301 /experts/; }` 同 host 同端口 | |
| 部署 reload nginx | |
| 验收：`curl -sI` 两条路径 | 最终 200 或 301→同站 `/experts/` 再 200；**grep -i 8443 必须空** |
| 浏览器打开无尾斜杠链接 | 专家目录可见 |

`gate-X1.md` · 证据 `X1/`

### X2 · 修 F2 隧道保活（P0）

| 做 | 过线 |
|----|------|
| 将 ECS→边缘 反向隧道改为 **systemd user/system unit**（或 supervisord 等价） | unit 文件进仓 `ops/edge/`（无密钥） |
| `Restart=always` + 合理 RestartSec | |
| 探活脚本：curl Chat 或 health 失败告警/日志 | `ops/edge/probe.sh` |
| 模拟：restart unit 后 60s 内 | Chat + /experts/ 200 |
| NOTES 写清依赖主机与端口（无密码） | |

`gate-X2.md`

### X3 · 配置与文档（F3/F4）

| 做 | 过线 |
|----|------|
| `ops/experts/catalog.yaml` 与现网 5 卡一致 | 进仓 |
| `ops/QUAD-FIX-DEPLOY-NOTES.md` 部署步骤+回滚（nginx/隧道/静态页） | |
| README/HANDOFF 专家链接用 **可无斜杠也能到** 的最终 URL | |
| 可选：LAUNCH 文件交叉链接到 QUAD-LAUNCH-* | |

`gate-X3.md`

### X4 · 回归 + 回写

| 做 | 过线 |
|----|------|
| Chat：要 1 课件 `/dl` | attachment · 空成功 0 |
| 专家台：无斜杠打开 + 1 卡进入 | 可用 |
| PIN 一句 CLAIM-QUAD-FIX-DEPLOY | |
| DEBT：F1/F2 关 | |
| Issue + push | |

`gate-X4.md` + REPORT

---

## 2. 证据目录

```text
ops/evidence/quad-fix-deploy/
  gate-X0.md … gate-X4.md
  X0/ X1/ X2/ X3/
ops/QUAD-FIX-DEPLOY-REPORT.md
ops/QUAD-FIX-DEPLOY-NOTES.md
ops/experts/catalog.yaml
ops/edge/*.service · probe.sh
```

---

## 3. 红线

- 假 full real · 假全校上线  
- 修入口却把专家台摘没  
- 密钥/SSH 密码进仓  
- 跳过 X1 只写文档  

---

## 4. 关联

- 调查：`ops/QUAD-FIX-SURVEY.md`  
- 卡：`ops/TASK-CARD-QUAD-FIX-DEPLOY.md`  
- 勾选：`ops/QUAD-FIX-DEPLOY-RUNBOOK.md`  
- 上游：`ops/QUAD-LAUNCH-REPORT.md` 深度审查结论  
