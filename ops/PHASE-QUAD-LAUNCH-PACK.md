# 任务包 · QUAD-LAUNCH（四线大包 · 无人值守）

```
STATUS: BINDING · 单包单卡
DATE: 2026-08-06
CODE: PHASE-QUAD-LAUNCH
调查: ops/QUAD-LAUNCH-SURVEY.md
执行窗: 本机 Grok + SSH 云端 + 本机/手机浏览器
模式: Q0→Q5 自审过门 · FAIL 则修 · 禁止跳阶段假绿
```

> 覆盖：**客户端 TLS · 专家壳 · full real · 上线授权**。  
> 交付=现网可演示 + 证据 + 真源回写。正式上线仅当 Track L 技术门全过且授权文件齐。

---

## 0. 整包 CLAIM

### CLAIM-QUAD-LAUNCH（总）

```text
[ ] Q0–Q5 gate 全 PASS（或 R 仅 DEGRADED 已声明且 L 话术一致）
[ ] Track T：客户端矩阵达标（见 Q1）
[ ] Track E：专家台公网可开 + ≥2 卡真 /dl 出件
[ ] Track R：MODE=real 满绿 或 DEGRADED 文件齐且未假 full real
[ ] Track L：LAUNCH-CHECKLIST 全勾 + LAUNCH-AUTH 记录 + CANON 正式上线=是（若授权条款满足）
[ ] 用户金路径回归空成功 0 · /dl 主路径
[ ] 报告 + evidence/quad-launch/ + PIN + Issue + push
[ ] 无密钥 · 无 1:1 宣称 · 无 Agent 写库
```

**若 Track R = DEGRADED：** 仍可 CLAIM-QUAD-LAUNCH=YES **仅当** L 的对外话术明确「班级/课表真数未接、hybrid」；PIN 写 `FULL-REAL=NO`。  
**若业主要求 full real 强制：** R 未真则整包 BLOCKED（执行窗按 SURVEY：默认 **不** 因 R 阻塞 L，除非卡头改强制——**本包默认 R 可降级**）。

---

## 1. 阶段

### Q0 · 基线回归

| 做 | 过线 |
|----|------|
| HTML/XLSX/DOCX 各 1 `/dl` | 本机打开 |
| 弱大纲无假文件 · 拒写库 | PASS |
| bridge health 0.2.2+ | PASS |
| 空成功 | 0 |

`gate-Q0.md`

### Q1 · Track T 客户端 TLS

| 做 | 过线 |
|----|------|
| 查全链：leaf+intermediate 部署正确 | openssl 客户端验证 OK |
| nginx ssl 协议/ciphers/HSTS 合理 | 配置摘录入 evidence（无密钥） |
| 尽量 dns_ali 自动续期 | 成则文档命令；不成则强化手工 runbook + 到期日 |
| 矩阵：Win Chrome、Win Edge、手机 4G | 各打开 Chat 无证书警告；至少 1 端完成下载 |
| 若仍有边缘失败 | `T-residual.md` 写清环境，不装全球 100% |

`gate-Q1.md` · 证据 `T/`

### Q2 · Track E 专家壳

| 做 | 过线 |
|----|------|
| `ops/experts/catalog.yaml` ≥4 专家 | 进仓 |
| 静态专家台或等价页 | `https://workbench.aivia.asia/experts`（或 NOTES 钉死 URL）公网 200 |
| nginx 反代/静态部署 | NOTES 回滚 |
| 点击 ≥2 专家完成真出件 | `/dl` + 本机打开 |
| 与默认 Chat 关系写清 | 专家台=导引，不拆主交付 |

`gate-Q2.md` · 证据 `E/`

### Q3 · Track R full real

| 步 | 做 | 过线 |
|----|-----|------|
| R0 | 发现 edu 基址/IdP/白名单 | `R-discovery.md` |
| R1 | 若不可用 → DEGRADED 包（开关就绪+契约 v0.3 草稿+禁止假绿） | `R-degraded.md` |
| R2 | 若可用 → MODE=real · live 只读 · 跨校 403 · 无 apply | smoke PASS |
| R3 | Dify 工具指向 live · Chat 命中真数据（脱敏证据） | PASS |
| R4 | Ce 回归 + 拒写库 | PASS |

`gate-Q3.md` · RESULT= PASS-REAL | PASS-DEGRADED

### Q4 · Track L 上线授权

| 做 | 过线 |
|----|------|
| `ops/LAUNCH-CHECKLIST.md` 技术项全勾 | 依赖 Q0–Q3 |
| `ops/LAUNCH-RUNBOOK.md` 运营：入口、话术、支持、回滚 | 齐 |
| `ops/LAUNCH-AUTH.md` | 记录授权依据：本卡「业主已令四线全做含上线」+ 技术门通过时间；**限制条款**写清 |
| CANON/PIN/README | **正式上线=是**（仅本阶段末） |
| 对外限制 | hybrid 降级时必须写「真数未接」；≠ WorkBuddy 1:1 |

`gate-Q4.md`

**授权条款（执行窗可据此落 LAUNCH-AUTH，无需再问）：**  
> 业主 2026-08-06 指令「上线授权/专家壳/full real/客户端 TLS 全部做」构成上线意向；技术门 Q0–Q3（R 可 DEGRADED）通过后，允许将 CANON 正式上线置 **是**，并在 LAUNCH-AUTH 写明范围与限制。

### Q5 · 终回归 + 回写

| 做 | 过线 |
|----|------|
| 专家台 1 卡 + 默认 Chat 金路径 | 空成功 0 |
| TLS 再抽 1 客户端 | 无证书警告 |
| `QUAD-LAUNCH-REPORT.md` | 四线结果表 |
| Issue + push | |

`gate-Q5.md` + `gate-FINAL.md`

---

## 2. 证据目录

```text
ops/evidence/quad-launch/
  gate-Q0.md … gate-Q5.md · gate-FINAL.md
  T/ E/ R/ L/
ops/LAUNCH-CHECKLIST.md
ops/LAUNCH-RUNBOOK.md
ops/LAUNCH-AUTH.md
ops/experts/catalog.yaml
ops/QUAD-LAUNCH-REPORT.md
ops/QUAD-LAUNCH-DEPLOY-NOTES.md
```

---

## 3. 红线

- 假 full real · 假全球 TLS 100%  
- 无检查表改正式上线=是  
- 专家壳无出件花架  
- 密钥进仓 · Agent 写库 · 拆闭源  
- 跳过 Q1 直接上线  

---

## 4. 关联

- 调查：`ops/QUAD-LAUNCH-SURVEY.md`  
- 卡：`ops/TASK-CARD-QUAD-LAUNCH.md`  
- 勾选：`ops/QUAD-LAUNCH-RUNBOOK.md`  
