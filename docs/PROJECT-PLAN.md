# Aivia Workbench · 项目总规划 v0.1

```
STATUS: BINDING 草案 · 2026-08-05
REPO: juanwan99/aivia-workbench
BASE: OpenWork (OpenCode) · Model: DeepSeek · Business: edu-core (later)
SUPERSEDES: pico 大功能主线（pico 仅维护/归档，不在此重复造壳）
```

---

## 1. 背景与决策

| 事实 | 含义 |
|------|------|
| Pico 长周期未稳住「出文档」 | 停止在旧栈上空转大包 |
| WorkBuddy 本机架构已 clean-room | 学 **响应逻辑**，不拆闭源 |
| 成品仓调研 | 选定 **OpenWork**（已拼好，内嵌 OpenCode） |
| 模型 | **DeepSeek** 钉死默认 |
| 业务 | **edu-core** 为事实真源；AI 为过程/产物真源 |

### 产品一句话

自然语言任务 → Agent 规划/工具执行 → **可验收产物** → 可停可重试 → 状态诚实。

### 非目标（v0.x）

- 像素级山寨 WorkBuddy  
- 重写 OpenCode Agent 核  
- 8h 集群 HA  
- 默认自托管大模型权重  
- Agent 直写 edu 成绩/学籍  

---

## 2. 成功定义

用户成功当且仅当：

1. 能登录或本机可用（阶段 A 可本机账号）  
2. 能下任务  
3. 过程可见（步骤/工具）  
4. **需要文件时，工作区或产物区有真文件可打开/下载**  
5. 能停、能再试  
6. 失败不显示假成功  

**工程成功 ≠ 产品成功。** 有文档无金路径不算过。

---

## 3. 阶段路线图

### 阶段 A · 跑通（Week 1～2）目标：能用

| ID | 交付 | 验收 |
|----|------|------|
| A1 | 文档化安装 OpenWork（Win 优先） | 新人按文档 1h 内打开 |
| A2 | 配置 DeepSeek BYOK | 对话/任务走 DS |
| A3 | 金路径 G1～G3 | 见 GOLD-PATHS |
| A4 | 记录 pin 版本（OpenWork/OpenCode） | `upstream/PIN.md` |

**出口：** G1（出 HTML/文件）稳定绿。

### 阶段 B · 纪律（Week 2～4）目标：不骗人

| ID | 交付 | 验收 |
|----|------|------|
| B1 | 交付硬规则 R1～R5 落地（Skill/配置/薄补丁） | 要文件无产物 → 不得成功 |
| B2 | 默认 Skills：课件 HTML、教案 DOCX 骨架 | 一键或一句话可触发 |
| B3 | 限流/超时/步数配置 | 防烧钱 |
| B4 | 品牌最小：应用名/关于（可选） | 不改交互骨架 |

**出口：** 多轮「要课件」10 次，空成功 = 0。

### 阶段 C · edu 桥（授权后）目标：身份进得来

| ID | 交付 | 验收 |
|----|------|------|
| C1 | edu JWT / 身份桥设计 + 原型 | school_id+membership 入账或侧车 |
| C2 | 只读 edu 工具（可选） | 不写业务库 |
| C3 | 变更提案位（S7 思路） | 人审后才进 edu |

**出口：** 演示教师用 edu 身份完成 G1。

### 阶段 D · 产品化（后）目标：可试点

- 教师试点班  
- 监控/配额  
- 是否 Web 门户包桌面能力（另立决策）  
- 上游跟进策略（submodule / 定期 merge）  

---

## 4. 组织与仓策略

| 仓 | 角色 |
|----|------|
| **aivia-workbench（本仓）** | 规划、Skills、桥、ops、补丁、真源文档 |
| **OpenWork 上游** | Agent 台与 OpenCode 核；能配置不 fork |
| **pico** | 旧线冻结；仅安全/停机级维护 |
| **edu-core** | 业务真源；本仓只适配 |

### 补丁策略

1. 优先：OpenWork 配置、Skills、MCP  
2. 其次：本仓 `bridge/` `skills/` 外挂  
3. 最后：最小 fork/patch 上游并记录 diff  
4. **禁止** 无 PIN 的大规模复制上游进本仓后改到无法回合并  

---

## 5. 里程碑（可勾选）

- [ ] M0 本仓规划合并（本文）  
- [ ] M1 OpenWork+DS 本机跑通  
- [ ] M2 G1 文件交付绿  
- [ ] M3 空成功清零  
- [ ] M4 edu 桥原型（授权后）  
- [ ] M5 小范围试点  

---

## 6. 风险与缓解

| 风险 | 缓解 |
|------|------|
| OpenWork 弱于 WB 办公生态 | Skills 自建课件；不指望腾讯文档引擎 |
| 上游 breaking | PIN 版本 + 变更日志 |
| 又做成套壳 | 金路径强制 tool 写盘 |
| 过早 edu 拖死 | C 阶段须授权，不挡 A/B |
| 双栈 Pico+本仓 | 明文：新功能只进本仓 |

---

## 7. 近期下一刀（立即）

1. 维护者本机安装 OpenWork  
2. 写入 `ops/INSTALL.md` + `ops/deepseek.env.example`  
3. 跑 G1，结果贴 Issue  
4. 不通过则记缺口；通过则开 B1 交付规则  

---

## 8. 相关链接

- OpenWork: https://github.com/different-ai/openwork  
- OpenCode: https://opencode.ai / https://github.com/anomalyco/opencode  
- 旧调研 pico#306 #307 #308  
- WorkBuddy：仅 clean-room 行为对标，禁止拆闭源  
