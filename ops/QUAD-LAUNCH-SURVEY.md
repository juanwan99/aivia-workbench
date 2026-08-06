# 调查 · 四线合一（上线授权 / 专家壳 / full real / 客户端 TLS）

```
DATE: 2026-08-06
STATUS: BINDING · 调查结论（实现前必读）
CODE: QUAD-LAUNCH-SURVEY
前提水位: CLAIM-WB-FIX-DEPLOY=YES · bridge 0.2.2 · workflow=fix-deploy · 正式上线=否 · hybrid
```

---

## 1. 业主指令

四条 **全部做**，一个大包：

1. **上线授权**（正式上线门禁与运营就绪）  
2. **专家壳**（对标 WorkBuddy 专家·技能入口的行为，名字可不同）  
3. **full real**（edu 真身份 + 真只读）  
4. **客户端 TLS**（解决/压实 Windows schannel 等边缘打不开）  

执行模式（与 WB-ALIGN 一致）：**无人值守分阶段自审**；FAIL 修到过线；禁止跳阶段假绿。

---

## 2. 现行水位（调查摘录）

| 维度 | 现状 | 证据 |
|------|------|------|
| 产品交付 | 课件/教案/表 `/dl`、上传再加工、交付清单、空成功纪律 | FIX-DEPLOY / SCENE-FULL |
| 管理 | metrics/audit/policy/quality · 日配额 | bridge 0.2.2 |
| 证书源站 | LE YE2 · workbench.aivia.asia · ~2026-11-03 | INFRA / NOTES |
| 客户端 TLS | 源站 OK；**部分 Windows schannel 失败** | FIX NOTES |
| edu | **MODE=hybrid** · fixture · 无 CLAIM-C-REAL full | EDU-BRIDGE · PIN |
| 专家壳 | MATRIX **E-01 跳过** · 仅多场景 prompt | ALIGN-STATUS |
| 正式上线 | **否** · 无 CLAIM-LAUNCH | CANON |

---

## 3. 分线调查结论

### 3.1 上线授权（Track L）

**不是** 改一句 CANON 就算上线。  
正式上线 = **产品授权 + 运营就绪 + 技术门禁齐** 的可审计包。

| 必须有 | 说明 |
|--------|------|
| 上线检查表 | 功能/安全/TLS/回滚/话术/支持通道 |
| 默认入口与品牌 | workbench 链、公告一句 |
| 监控与配额 | ops metrics + 日限额策略已生效 |
| 事故回滚 | workflow/bridge 回滚步骤（NOTES 已有可升格） |
| 对外话术 | 能说什么 / 不能说（≠1:1 WorkBuddy） |
| **业主授权记录** | Issue 评论或 `ops/LAUNCH-AUTH.md` 签字式条目（执行窗在通过技术门后 **代填「待业主确认」或按卡内授权条款」**） |

**依赖：** Track T 至少「源站+主流浏览器矩阵绿」；Track E 最小专家入口可点；Track R **不阻塞上线**（可 hybrid 上线，但必须写清「班级真数未接」）。  
**风险：** 把 hybrid 说成全校教务已通 = 假上线。

### 3.2 专家壳（Track E）

对标 WorkBuddy `专家·技能·连接器`（live-05）：**可浏览能力目录 → 进入可执行任务**。

| Aivia 可落点（clean-room） | 不做 |
|---------------------------|------|
| **Web 专家台**：静态/轻前端页或 Dify 多应用入口页 | 抄 WB 像素/侧栏六宫格 1:1 |
| 专家卡 → 深链到 **专用 Chat/App** 或带 query 的场景 | 桌面 cwd 专家 |
| 分类含「教育学习」等 | 假专家无后端 |
| 管理侧：卡清单 YAML/MD 配置，非写死仅一处 | 把治理按钮塞进单 Chat 墙 |

**最小可交付（本包高标准）：**

1. 公网可打开 `https://workbench.aivia.asia/experts`（或 `/go` 专家台，nginx 反代静态）  
2. ≥4 张专家卡（课件 / 教案 / 报表 / 大纲·研究）  
3. 点击进入可用对话并完成 **1 次真 `/dl` 出件**（至少 2 卡实测）  
4. 配置源进仓 `ops/experts/catalog.yaml`（无密钥）  

### 3.3 full real（Track R）

| 现状 | 缺口 |
|------|------|
| hybrid + exchange 闸门 + fixture classes/courses | edu-core **live 只读 API**、真 IdP/JWT 校验 |
| Dify 可调 bridge 容器网 | MODE=real 契约 v0.3、跨校 403、Ce 回归 |

**关键依赖（调查钉死）：**  
若执行时 **仍无** edu-core 内网只读基址与契约，则：

- 完成 **R-DISCOVERY** 书面：`ops/evidence/quad-launch/R-discovery.md`  
- 实现 **最大可做**：契约升版草稿、fixture 对齐真 schema、Dify 工具挂载保持、MODE 切换开关代码就绪  
- **CLAIM-C-REAL full 不得绿**；整包可用 `TRACK-R=DEGRADED` 但必须 **阻塞「宣称真数已通」**  
- **不阻塞** Track L（上线话术写清 hybrid）

若 edu API **已就绪**：必须 MODE=real · live 数据证据（脱敏）· smoke · 禁写库。

### 3.4 客户端 TLS（Track T）

| 已确认 | 待查/待做 |
|--------|-----------|
| 源站 LE YE2、SNI、HTTPS 200 | 完整链（中间证）、OCSP/stapling |
| curl/openssl 服务器侧绿 | **Windows Chrome/Edge/schannel** 多网络矩阵 |
| 历史 RST/WAF 偶发 | nginx ssl 配置、TLS1.2/1.3、ALPN、是否缺链 |
| 续期手工 DNS-01 | **dns_ali 自动续期**（AK 仅服务器）优先落地 |

**高标准验收：**

1. 证书链完整（客户端不报「证书不完整」）  
2. Windows 10/11 · Chrome + Edge 各至少 1 次：打开 Chat + 下 1 文件  
3. 手机 4G 打开 Chat（证书无警告）  
4. 续期策略可执行（自动或日历+runbook）  
5. 证据：`openssl crl/chain` 输出 + 客户端截图（可打码）  

---

## 4. 依赖与推荐串行（无人值守）

```text
Q0  总基线回归（FIX-DEPLOY 金路径）
Q1  Track T 客户端 TLS（先稳打开）
Q2  Track E 专家壳（入口产品化）
Q3  Track R full real（发现→real 或 DEGRADED）
Q4  Track L 上线授权（技术门全过 → 授权包 → CANON 正式上线）
Q5  终回归 + 回写
```

**理由：** 打不开谈不上线；有专家台才像「工作台」；真数可降级；**上线放最后** 避免假绿。

---

## 5. 风险总表

| 风险 | 缓释 |
|------|------|
| edu API 缺失 | R 降级条款；禁止假 full real |
| 上线话术过度 | LAUNCH 脚本强制写限制 |
| TLS 边缘非源站问题 | 矩阵分路径；不装 100% 全球 |
| 专家壳变花架子 | 强制 2 卡真出件 |
| 范围膨胀 PPT/IM/桌面 | 本包不做 |

---

## 6. 调查结论一句话

四线可一个大包串行：先 TLS 与专家壳做硬，full real 能真则真否则诚实降级，最后上线授权包；**全部要有可勾选高标准验收，禁止只改文档。**
