# 阶段 A 执行大包（写实版）

```
STATUS: BINDING · 阶段 A 唯一执行包
DATE: 2026-08-05
对齐: docs/CANON.md · HANDOFF · GOLD-PATHS
出口: G0 + G0b + G1 + G1+ 全绿 → 回写 PIN + Issue #1
```

## 0. 产品底线（对标主流站的最小集，不是花架子）

对标的是 **ChatGPT / Gemini / Grok 类站点的使用真相**，不是抄 UI：

| 用户默认真相 | 阶段 A 必须做到 |
|--------------|----------------|
| 打开就能进 | 浏览器打开工作台 URL，能登录（G0） |
| 一句话有反应 | DeepSeek 短聊可用（G0b） |
| 要文件有文件 | 要 HTML 课件 → **可下载**（G1） |
| 改一版还有文件 | 同会话再改 → **仍有可下载产物**（G1+） |
| 失败不装成功 | 无文件不得标完成（G4 建议同日） |

**不做装完就宣称对标完成。** A 只证明：现网 Web 入口 + 模型 + 默认交付链是真的。

---

## 1. 范围

| 做 | 不做 |
|----|------|
| 现网 Docker Dify | 阶段 B 十次空成功清零精修 |
| 反代 / 建议 workbench 子域 | edu 桥 |
| DeepSeek | OpenWork 主线 |
| **一条默认「课件」入口**（对话或发布应用） | 像素抄主流站 |
| G0 / G0b / G1 / G1+ | 改 pico 大功能 |
| PIN + Issue #1 | 密钥进仓 |

基建策略：沿用现网服务器/IP/`aivia.asia`（见 `ops/INFRA.md`）。具体 IP/SSH **不进 Git**。

---

## 2. 执行顺序（一次做完，中间不换大题）

### A0 摸底

- [ ] 机器可 SSH；Docker Compose 可用（建议 ≥ 2.24）
- [ ] 内存/磁盘够用；80/443 与现有 Pico 反代关系清楚
- [ ] DeepSeek Key 已备（仅服务器/控制台）
- [ ] 入口计划：`workbench.aivia.asia` 或临时 `IP:端口`

### A1 安装 Dify

```bash
git clone --branch "$(curl -s https://api.github.com/repos/langgenius/dify/releases/latest | jq -r .tag_name)" \
  https://github.com/langgenius/dify.git
cd dify/docker && cp .env.example .env
docker compose up -d && docker compose ps
```

官方文档为准：https://docs.dify.ai  
通过：容器健康；能开 `/install`。

### A2 入口

- Host 分流：`pico.*` 旧站保留；`workbench.*` → Dify
- HTTPS 优先；无 DNS 时允许 IP 内测，正式前补域

通过：浏览器打开约定 URL 见 Dify，不是误进 Pico。

### A3 G0

- 初始化管理员并登录  
通过：主界面可用。

### A4 G0b

- 模型供应商 → DeepSeek → 短聊「只回：好」  
通过：回复「好」。

### A5 默认入口（反花架子关键步）

必须有一条**普通人能点到的路径**，满足：

1. 从工作室/探索/对话入口进入，**不必先会画布**
2. 系统提示或工作流明确：**需要课件时必须给出可下载文件**；禁止只贴长代码当成功
3. 模型固定走 DeepSeek

推荐：发布一个「课件助手」Chatbot/Agent（或 Chatflow 末节点出文件）。名称示例：`Aivia 课件（阶段A）`。

### A6 G1

用户话术（可照念）：

> 请做一份初中生物「豌豆杂交」HTML 课件，要能下载打开。

通过：

- [ ] 有过程（步骤/节点/工具任一可见）
- [ ] **可下载** `.html`（或平台可打开产物链接）
- [ ] 用浏览器打开内容与主题相关（不要求完美美工）
- [ ] 无文件则 **FAIL**，不得标成功

### A7 G1+（阶段 A 出口加严）

**同一会话**继续：

> 请在上一份基础上再增加 3 道练习题，并给出更新后的可下载 HTML。

通过：

- [ ] 再次得到可下载文件（新文件或明确覆盖说明）
- [ ] 打开后能看到新增练习相关内容
- [ ] 仍禁止「只在聊天里改字、无文件」

### A8 建议 G4（同日）

故意中断或制造失败后，界面**不**显示「已完成但无文件」。

### A9 回写

1. `upstream/PIN.md`：Dify tag、DeepSeek 模型 id、日期  
2. Issue #1：URL、G0/G0b/G1/G1+ 结果、产物文件名（无 Key）  
3. 实际子域/端口若与文档示例不同 → 改 `ops/INFRA.md` 一句  

---

## 3. 完成定义（全部勾上才算阶段 A 绿）

```text
[ ] G0 PASS
[ ] G0b PASS
[ ] G1 PASS（可下载 HTML）
[ ] G1+ PASS（改后仍可下载）
[ ] 默认入口存在（非仅管理员私有草稿）
[ ] PIN 已填
[ ] Issue #1 已贴结果
[ ] 无密钥进仓
```

未全绿 → 记缺口，**不自 PASS**，不进入阶段 B 宣称。

---

## 4. 关联文件

| 文件 | 用途 |
|------|------|
| `ops/INSTALL.md` | 安装摘要 |
| `ops/INFRA.md` | 域名/同机策略 |
| `docs/GOLD-PATHS.md` | 金路径定义（含 G1+） |
| `ops/G-PATH-RUNBOOK.md` | 现场勾选 |
| `docs/DELIVERY-RULES.md` | 交付纪律（B 深化，A 已预埋） |
