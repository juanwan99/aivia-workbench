# Aivia Workbench · 项目总规划 v0.3

```
STATUS: BINDING · 2026-08-05
REPO: juanwan99/aivia-workbench
BASE: Dify (Web) · Model: DeepSeek · Business: edu-core (later)
UPDATED: 阶段 A 功能出口收口；M1/M2 按 PIN 勾选；下一刀 = 入口硬化 + 阶段 B
```

---

## 1. 背景与决策

| 事实 | 含义 |
|------|------|
| Pico 出文档不稳 | 换底座 |
| 产品 = 浏览器公网工作台 | Web 主路径 |
| 选型 v2 + 业主拍板 | **Dify** + DeepSeek + 现网 |
| OpenWork | 二期本地增强 |

### 产品一句话

打开域名 → 登录 → 任务 → Agent/工作流 → **可下载产物** → 可停可重试 → 状态诚实。

### 非目标（v0.x）

- 像素山寨 WorkBuddy / 乱 fork Dify 核 / OpenWork 默认入口  
- Agent 直写 edu / OnlyOffice 全量（后置）  

---

## 2. 成功定义

1. 浏览器能打开工作台  
2. 能登录、下任务、过程可见  
3. 要文件时有**可下载真文件**  
4. 失败不假绿  

工程绿 ≠ 产品绿。

---

## 3. 阶段路线图

### 阶段 A · 跑通 — **功能出口已收（2026-08-05）**

| ID | 交付 | 状态 |
|----|------|------|
| A1 | 现网 Docker Dify + 子域 | **Done** · Dify 1.16.1 |
| A2 | DeepSeek | **Done** · deepseek-chat |
| A3 | G0 / G0b / G1 / G1+ | **Done** · 见 PIN |
| A4 | PIN | **Done** |
| A-hardening | 正式证书 + 公网可达 + G4 | **OPEN** · CLOSEOUT R-A* |

**出口（功能）：** G0+G0b+G1+G1+ 绿。  
**产品可用：** 须清 R-A1/R-A2（见 `ops/PHASE-A-CLOSEOUT.md`）。

### 阶段 B · 纪律（下一步主战场）

| ID | 交付 | 验收 |
|----|------|------|
| B1 | 交付硬规则落地 | 要文件无产物 → 不得成功 |
| B2 | 课件 HTML / 教案 DOCX | 一句话可触发可下载 |
| B3 | 限流/超时/配额 | 防烧钱 |
| B4 | 品牌最小 | 可选 |
| B5 | 中心知识库/模板 | 平台治理 |

**出口：** 多轮「要课件」**10 次**，空成功 = **0**。

### 阶段 C · edu 桥（授权后）

身份桥 + 只读/提案；不直写业务库。

### 阶段 D · 试点

小范围教师；监控；可选 OnlyOffice / 本地客户端。

---

## 4. 仓策略

| 仓 | 角色 |
|----|------|
| aivia-workbench | 规划、ops、应用资产、桥 |
| Dify 上游 | 主台；少 fork |
| pico | 冻结 |
| edu-core | 业务真源 |

---

## 5. 里程碑

- [x] M0 规划 + CANON  
- [x] M1 现网 Dify + DS 可登录（PIN）  
- [x] M2 G1/G1+ 文件可下载（PIN · **功能**）  
- [ ] M2b 入口硬化（正式证书 + 公网无 403）  
- [ ] M3 空成功清零  
- [ ] M4 edu 桥  
- [ ] M5 试点  

---

## 6. 风险

| 风险 | 缓解 |
|------|------|
| 自签/WAF 拦教师 | CLOSEOUT R-A1/R-A2 优先 |
| 又成套壳闲聊 | G1 强制 + B 十次尺子 |
| 双主线回潮 | CANON/HANDOFF |

---

## 7. 近期下一刀

1. 消化 `ops/PHASE-A-CLOSEOUT.md` 残留（证书、可达、建议 G4）  
2. 开阶段 B：DELIVERY-RULES 落地 + 10 次要课件  
3. 结果回写 Issue #1  

---

## 8. 链接

- Dify: https://github.com/langgenius/dify  
- PIN: [upstream/PIN.md](../upstream/PIN.md)  
- CLOSEOUT: [ops/PHASE-A-CLOSEOUT.md](../ops/PHASE-A-CLOSEOUT.md)  
