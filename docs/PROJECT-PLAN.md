# Aivia Workbench · 项目总规划 v0.2

```
STATUS: BINDING · 2026-08-05
REPO: juanwan99/aivia-workbench
BASE: Dify (Web, self-host) · Model: DeepSeek · Business: edu-core (later)
SUPERSEDES: pico 大功能主线；并覆盖 2026-08-05 前「OpenWork 桌面主线」表述
```

---

## 1. 背景与决策

| 事实 | 含义 |
|------|------|
| Pico 未稳住「出文档」 | 停止旧栈大包 |
| 产品定义 = 浏览器/公网工作台 | 主路径必须是 Web |
| 云端优先 + 现网服务器/域名 | Docker 自托管挂现网 |
| 选型调查 v2 | **Dify** 作主底座 |
| 模型 | **DeepSeek** |
| 业务 | **edu-core** 后置桥；AI 不直写业务库 |
| OpenWork | **二期**本地增强，非主线 |

### 产品一句话

打开域名 → 登录 → 自然语言任务 → Agent/工作流执行 → **可下载产物** → 可停可重试 → 状态诚实。

### 非目标（v0.x）

- 像素级山寨 WorkBuddy  
- 乱 fork / 重写 Dify 核  
- 以桌面 OpenWork 为默认入口  
- 8h 集群 HA  
- 默认自托管大模型权重  
- Agent 直写 edu 成绩/学籍  
- OnlyOffice 全量精修（后置可选）  

---

## 2. 成功定义

用户成功当且仅当：

1. 浏览器能打开工作台（HTTPS 子域或现网 URL）  
2. 能登录  
3. 能下任务；过程可见  
4. **需要文件时，有可下载真文件**（HTML/DOCX/PPTX 等）  
5. 能停、能再试  
6. 失败不显示假成功  

**工程成功 ≠ 产品成功。** 有文档无金路径不算过。

---

## 3. 阶段路线图

### 阶段 A · 跑通（Week 1～2）目标：能用

| ID | 交付 | 验收 |
|----|------|------|
| A1 | 现网 Docker 安装 Dify + 反代/子域 | 浏览器打开工作台 |
| A2 | 配置 DeepSeek 模型供应商 | 对话/应用走 DS |
| A3 | 金路径 G0～G1（浏览器） | 见 GOLD-PATHS |
| A4 | 记录 pin（Dify 镜像/tag） | `upstream/PIN.md` |

**出口：** G1（浏览器可下载 HTML/文件）稳定绿。

### 阶段 B · 纪律（Week 2～4）目标：不骗人

| ID | 交付 | 验收 |
|----|------|------|
| B1 | 交付硬规则落地（应用提示/工作流强制出件） | 要文件无产物 → 不得成功 |
| B2 | 默认课件应用：HTML / 教案 DOCX（或工作流） | 一句话可触发且可下载 |
| B3 | 限流/超时/配额 | 防烧钱 |
| B4 | 品牌最小（站点名/关于，可选） | 不改交互骨架乱造 |
| B5 | 中心知识库/模板（平台侧） | 教师可选用，非本机建库依赖 |

**出口：** 多轮「要课件」10 次，空成功 = 0。

### 阶段 C · edu 桥（授权后）

| ID | 交付 | 验收 |
|----|------|------|
| C1 | edu JWT / 身份桥设计 + 原型 | school_id+membership 入会话或侧车 |
| C2 | 只读 edu 工具（可选） | 不写业务库 |
| C3 | 变更提案位 | 人审后才进 edu |

### 阶段 D · 产品化（后）

- 教师小范围试点  
- 监控/配额  
- OnlyOffice 等在线精修（可选）  
- **本地客户端（OpenWork 等）可选**，另立决策，不冲主入口  

---

## 4. 组织与仓策略

| 仓/上游 | 角色 |
|---------|------|
| **aivia-workbench** | 规划、ops、应用/工作流资产、桥、真源文档 |
| **Dify 上游** | Web 主台；配置与应用优先，少 fork |
| **pico** | 旧线冻结 |
| **edu-core** | 业务真源；本仓只适配 |
| OpenWork（optional） | 二期本地；见 `ops/INSTALL-OPENWORK-optional.md` |

### 补丁策略

1. 优先：Dify 配置、应用、工作流、知识库  
2. 其次：本仓 `bridge/`、模板、ops  
3. 最后：最小补丁并记录 PIN  
4. **禁止** 无 PIN 的大规模改核到无法回合并  

---

## 5. 里程碑

- [x] M0 本仓规划（含口径切换至 Dify Web）  
- [ ] M1 现网 Dify + DS 浏览器可登录  
- [ ] M2 G1 文件可下载绿  
- [ ] M3 空成功清零  
- [ ] M4 edu 桥原型（授权后）  
- [ ] M5 小范围试点  

---

## 6. 风险与缓解

| 风险 | 缓解 |
|------|------|
| Dify 工作流未强制出件 | 金路径 + 交付规则 + 应用设计 |
| 上游 breaking | PIN + 官方升级说明 |
| 又做成套壳闲聊 | G1/G2 强制可下载文件 |
| 过早 edu | C 须授权，不挡 A/B |
| 双主线回潮 | HANDOFF 禁止 OpenWork 占主入口 |

---

## 7. 近期下一刀（立即）

1. 现网按 `ops/INSTALL.md` Docker 部署 Dify  
2. 反代挂子域（如 workbench.aivia.asia）  
3. 配置 DeepSeek → 跑浏览器 G1  
4. 回写 Issue #1 + `upstream/PIN.md`  

---

## 8. 相关链接

- Dify: https://github.com/langgenius/dify · 文档 https://docs.dify.ai  
- DeepSeek: https://platform.deepseek.com  
- 选型: [SELECTION-WEB-v2.md](./SELECTION-WEB-v2.md)  
- WorkBuddy：仅 clean-room 行为对标，禁止拆闭源  
