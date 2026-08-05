# 阶段 C · 修复完善 + 部署包

```
STATUS: BINDING · CLAIM-C(mock) 审查后唯一执行包
DATE: 2026-08-05
CODE: PHASE-C-FIX-DEPLOY
对齐: PHASE-C-PACK · C-PATH-RUNBOOK · 深度审查债
前提: CLAIM-C YES (MODE=mock) · E1 后置 · CLAIM-B NO
出口: 部署可复活 + 密钥强制 + Dify 挂载可证 + 烟测锁 401/403/apply + 真源无滞后
```

> **不重做 C 大叙事。** 只清审查债并完成可运维部署。  
> **不**因本包宣称 CLAIM-B 或 real edu 已通。

---

## 0. 审查债清单 → 本包映射

| 审查债 | 严重度 | 本包 |
|--------|--------|------|
| DEBT-LEDGER 滞后 | 中 | F0 |
| 默认 JWT secret | 高 | F1 |
| mock exchange 无鉴权 · 误暴露风险 | 高 | F1 + D2 |
| Dify 工具是否真挂载未钉 | 中 | F2 |
| 无自动化烟测 | 中 | F3 |
| openapi servers 写死 IP | 低 | F4 |
| audit 过滤偏松 | 低 | F4 |
| 进程无 systemd/compose 复活 | 中 | **D1** |
| 反代/仅本机绑定文档 | 中 | **D2** |
| real edu 未接 | — | **OUT**（另卡） |
| E1 证书 | — | **OUT**（后置） |

---

## 1. 修复包 F（应用/代码/治理）

### F0 · 真源扫尾（必做 · 快）

- [ ] `ops/DEBT-LEDGER.md`：C = CLAIM-C 绿(mock)；下一刀 = 本包  
- [ ] CANON/HANDOFF/README 下一刀指向 FIX-DEPLOY  
- [ ] Issue 标题/评论同步  

### F1 · 密钥与换票硬化（高 · 必做）

| 项 | 要求 |
|----|------|
| 启动 | `BRIDGE_JWT_SECRET` **未设或等于默认弱值 → 拒绝启动**（exit 非 0） |
| 密钥位置 | 仅 `~/.secrets/bridge.env` 或 systemd EnvironmentFile（**不进 Git**） |
| mock exchange | 保留 mock，但增加 **可选** `BRIDGE_EXCHANGE_TOKEN`：若设置则请求头/body 必须匹配才发 JWT |
| 文档 | README/RUNBOOK 写明：生产半公开前必须设 exchange token 或关掉 exchange 改走真 IdP |

验收：无 secret 启动失败；有 secret 健康检查 200；错误 secret exchange 401/403。

### F2 · Dify 运行时挂载（中 · 必做）

目标：不只是 curl 通，**默认课件相关能力能调 bridge 或书面证明「仅侧车 API、Dify 后挂」**。

**路径甲（推荐）：**  
1. 控制台导入/配置 `bridge/openapi.json` 自定义工具  
2. 工具鉴权：Bearer 来自测试 JWT（先 exchange）  
3. 在「Aivia 课件」或专用「Aivia 身份演示」应用中挂 `list_my_classes` / `get_course_meta` / `create_proposal`  
4. 跑一轮：带身份问「本校有哪些班」→ 工具命中 mock 数据  

**路径乙（书面缩 scope）：**  
Issue 钉死：「C mock 仅 API/Ce 金路径；Dify 工具挂载后置到 real」——**须业主可见**，不得假装已挂。

验收：甲则截图/文字记工具名+一次成功调用；乙则 Issue 书面。

### F3 · 烟测脚本（中 · 必做）

新增 `bridge/smoke.sh`（或 `bridge/tests/smoke.sh`）：

```text
1) health 200
2) 无 token → /me 401
3) exchange teacher → /me school_id
4) 跨校 classes → 403
5) create_proposal → pending
6) apply → 403
7) teacher review → 403；admin review approve/reject → 200
8) exp 过期 token → 401（可短 TTL 测或伪造）
```

退出码：全过 0，否则非 0。  
CI 可选；**现网部署后必须跑一次**并把摘要贴 Issue。

### F4 · 小清理（建议同日）

- openapi `servers[0].url` 改为 `http://127.0.0.1:18090/bridge/v1` + 注释「部署时改」  
- audit 列表默认只返回本 `school_id` 相关事件（无 school 字段的 exchange 可保留或打标）  
- 版本号保持 0.1.x 或 bump 0.1.1 写 PIN  

---

## 2. 部署包 D（现网可复活）

### D1 · 进程守护

任选其一（钉死一种进 PIN）：

| 方式 | 要点 |
|------|------|
| **systemd**（推荐） | `aivia-bridge.service`：User=ops，EnvironmentFile=`/home/ops/.secrets/bridge.env`，`ExecStart=.../bridge/run.sh`，Restart=on-failure |
| docker compose | 仅 bridge 服务，network host 或挂到 dify 可达网段，**不**把 18090 无脑映射公网 0.0.0.0 |

验收：

```bash
systemctl start aivia-bridge   # 或 compose up -d
curl -sS http://127.0.0.1:18090/bridge/v1/health
# 重启机器或 kill 后自动起来（systemd）/ 文档写明 compose 策略
```

### D2 · 网络暴露策略（硬）

| 项 | 要求 |
|----|------|
| 默认 | `BRIDGE_HOST=127.0.0.1` **仅本机** |
| 若 Dify 容器调 bridge | 用 docker 网桥 IP / `host.docker.internal` / 宿主机内网 IP，**勿** `0.0.0.0` 对公网 |
| 反代 | 若必须 `/bridge` 上域名：强制鉴权 + 内网或 IP 允许列表；**禁止**匿名 exchange |
| E1 后置 | 自签环境下更不要公网裸奔 bridge |

验收：外网直接扫 18090 应不通（或 403）；本机 health 200。

### D3 · 运维手册三行

写入 `bridge/README.md` + `ops/INFRA.md` 一句：

```text
启: systemctl start aivia-bridge
验: curl 127.0.0.1:18090/bridge/v1/health
烟: bash bridge/smoke.sh
密: ~/.secrets/bridge.env
```

### D4 · 部署后回归（必做）

| ID | 项 |
|----|-----|
| R1 | smoke.sh 全绿 |
| R2 | G1 课件 DOWNLOAD_READY 仍绿 |
| R3 | Ce2 跨校仍 403（经 smoke 或手工） |
| R4 | PIN 更新 bridge 部署方式 + 版本 |

---

## 3. 完成定义（CLAIM-C-FIX）

```text
[ ] F0 真源无「C 仍进行中」滞后
[ ] F1 无弱 secret 可启动；secret 仅服务器
[ ] F2 Dify 已挂工具 或 书面后置钉死
[ ] F3 smoke.sh 现网 PASS
[ ] D1 守护进程可复活
[ ] D2 暴露策略合规（默认本机）
[ ] D4 R1–R4
[ ] Issue 回写（无 Key）
[ ] 未勾 CLAIM-B；未假称 real edu
```

**本包绿 ≠ real edu。** real 另卡 `PHASE-C-REAL`。

---

## 4. 禁止

- 重刷完整 B / 未授权改 CLAIM-B  
- Agent apply / 直写 edu  
- JWT secret / exchange token 进 Git  
- 公网无鉴权开放 exchange  
- fork Dify 核  

---

## 5. 关联

| 文件 | 用途 |
|------|------|
| `ops/C-FIX-DEPLOY-RUNBOOK.md` | 勾选 |
| `bridge/server.py` | F1/F4 改代码 |
| `bridge/smoke.sh` | F3 |
| `bridge/openapi.json` | F2/F4 |
| `upstream/PIN.md` | 部署钉 |
