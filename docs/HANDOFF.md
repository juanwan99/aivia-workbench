# Aivia Workbench · 交接文档（新窗必读）

```
STATUS: BINDING · 新窗总管开场真源之一
DATE: 2026-08-06
UPDATED: CLAIM-S4-CAP=FULL YES · CLAIM-S4.1-HOTFIX=YES · CLAIM-S3-UX=YES · 下一刀=维护态
仓: https://github.com/juanwan99/aivia-workbench
冲突裁决: docs/CANON.md > 本文 > 任何旧任务卡/旧 CLAIM 叙事
```

> **新窗接替后：先读本文 §1–§4，再读 CANON，再动手。**  
> **禁止** 一上来修证书/备案/教育专家站/堆运维 CLAIM。  
> **宏观目标错了 = 整窗工作作废。**

---

## 1. 宏观目标（背下来 · 不可再偏）

### 1.1 产品是什么

**通用 AI 任务工作台（Web）。**  
对标 **WorkBuddy 行为**（clean-room，不拆闭源）：

```text
人用自然语言派活 → Agent 多步执行 → 交出真结果（文件/代码/文案/表/分析…）
```

- **能力默认通用：什么都能干。**  
- 同一入口应能支撑例如：  
  **编程 · 炒股/行情分析 · 公众号文案 · 周报/纪要 · 表格 · 改稿 · 研究整理…**  
- **任务具有通用性**，不是先选「学科专家」才能干活。

### 1.2 教育与 edu-core 放哪

| | 正确 |
|--|------|
| 教育 | 只是 **众多领域之一**，不是产品定义 |
| edu-core | **干教育且需要学校真数据时再接通**（只读） |
| 任何时候 | **禁止** Agent 直写成绩/教务业务库 |

没有教育任务时，**不依赖、不主推、不验收 edu**。

### 1.3 技术底座（手段 · 不是目标本身）

| 层 | 现状 |
|----|------|
| 形态 | 浏览器 / 公网 Web（Dify） |
| 模型 | 默认 **DeepSeek**（内容能力主要靠模型 API） |
| 编排 | Dify 工作流/应用 · **App=Aivia 通用 Agent** · workflow=`general-wb-s1` |
| 交付 | https **`/dl`** 真文件（禁空成功、禁 data-URL 主路径） |
| 对标方式 | WorkBuddy **行为** clean-room；名字可不同 |

### 1.4 怎样才算「做成了」（宏观验收）

同一默认入口，**跨领域** 多条真实任务：

1. 接得住（通用，不锁死教育）  
2. 做得完（有执行，非纯闲聊）  
3. 交得出（要文件则真可下可开；短答不硬塞文件）  
4. 改得动（同会话改一版）  
5. 失败诚实  

**禁止：** 用「一条生物课件绿」或「运维/证书 CLAIM」冒充对标 WorkBuddy 完成。

---

## 2. 正本清源（错误支线 · 必须忘掉）

### 2.1 曾犯的错（不要重复）

| 错误 | 为何错 |
|------|--------|
| 把产品做成 **教育专家站**（五张教研卡） | 违背「能力通用 / 什么都能干」 |
| 把 **对标 WorkBuddy** 收成课件/教案验收 | WorkBuddy 是 **通用任务台** |
| 多轮「优化」停在 **证书/隧道/边缘域名/上线话术** | 业主体感零变化；**不是** 宏观目标 |
| 有 WorkBuddy **深查** 却未按通用能力落地 | 调查有、执行偏 |
| 空成功、假下载 | 铁律禁止 |

### 2.2 已作废为主线的叙事

详见 `docs/MEMORY-RESET.md` · `ops/SUPERSEDED.md`：

- 「主线 = 教研五卡 / 教育垂直」→ **废**  
- 「对标完成 = QUAD 上线 / FIX 运维绿」→ **废**  
- 「下一刀必须 = 备案迁回 / dns_ali / full real」→ **废为主线**（除非业主 **明文单开** 且声明非产品核心）  

历史 `ops/evidence/**` 可留档；**与 CANON 冲突以 CANON 为准**。

### 2.3 可保留的工程底盘（水管）

- Dify + DeepSeek + bridge **`/dl`** 真文件能力  
- 空成功纪律、打包 OOXML/HTML 等 **须服务全领域任务**  
- 公网可达入口（现网域名以 README/PIN 为准，如 asyncova 边缘）— **运维事实 ≠ 产品完成**  

---

## 3. 必读顺序（新窗开场）

```text
1) 本文 docs/HANDOFF.md          ← 宏观 + 清源
2) docs/CANON.md                 ← 唯一正本
3) docs/MEMORY-RESET.md          ← 作废清单
4) ops/SUPERSEDED.md             ← 旧卡降级表
5) ops/TASK-CARD-GENERAL-WB.md   ← 现行唯一产品主卡
6) ops/PHASE-GENERAL-WB-PACK.md  ← 包
7) ops/S1-GENERAL-WB-REPORT.md   ← S1 已收（W0+G1–G3）
（可选）ops/WB-FEATURE-MATRIX.md / WB-ORG-MODEL.md / WB-RESPONSE-LOGIC.md
        → 仅作「通用能力」参考，禁止再收成教育验收
```

**不要** 把旧 QUAD / 教育 ALIGN 卡当下一刀。

---

## 4. 现行下一刀

| 项 | 内容 |
|----|------|
| **主卡** | `ops/TASK-CARD-GENERAL-WB.md` |
| **已收** | **CLAIM-GENERAL-WB** · **S3-UX** · **S4-CAP FULL**（S4.1） |
| **下一刀** | **维护态** · 或业主点名 |
| **包** | `ops/PHASE-GENERAL-WB-PACK.md` |
| **S3/S4 报告** | `ops/S3-UX-REPORT.md` · `ops/S4-CAP-REPORT.md` · `ops/S4.1-HOTFIX-REPORT.md` |
| **执行窗** | 本机浏览器真测 + 轻量探针；**体感变化** 为准 |
| **出口纪律** | 行为对标 · **≠** 像素 · **≠** 备案/运维绿 · **≠** 教育站 |

### 验收纪律（写进执行习惯）

- 推荐问题 / 系统提示必须是 **通用 Agent**，不是「仅教研」  
- 证据：`ops/evidence/general-wb/` 浏览器/API 真跑（S1 已在 `s1/`）  
- 教育课件 **最多加分项**，不得替代跨领域电池  
- edu-core full real：**非本卡默认范围**  

---

## 5. 硬禁令（新窗）

1. 禁止再把宏观目标改成教育站或运维工程  
2. 禁止空成功、data-URL 主路径、`[blocked]` 报绿  
3. 禁止 Agent 写 edu/业务库  
4. 禁止密钥进仓  
5. 禁止拆 WorkBuddy 闭源 / 假 1:1 像素抄  
6. 禁止无跨领域体感证据宣称「已对标 WorkBuddy」  
7. 禁止备案/dns_ali/full real 占用主线（除非业主新指令单开）  

---

## 6. 状态快照（交接时点）

```text
【宏观】通用任务工作台 · 对标 WorkBuddy 行为 · 什么都能干
【教育】后接 edu-core（只读）；非主线
【底盘】Dify + DeepSeek + /dl · 可用水管
【清源】MEMORY-RESET 已生效 · 教育/QUAD 主叙事作废
【S1】FULL YES · 通用入口 G1–G3
【S1.1】YES · /experts 通用化
【S2】CLAIM-GENERAL-WB=FULL YES · S2.1 审查债关
【S3】CLAIM-S3-UX=YES · U1–U7 体感门
【S4】CLAIM-S4-CAP=FULL YES · S4.1 关 C2 套娃
【证据】ops/evidence/general-wb/s1/…/s4.1/
【Chat】https://asyncova.com/chat/lOMVPbz7rZmbJSJl
【experts】https://asyncova.com/experts
【App】Aivia 通用 Agent · workflow=general-wb-s4.1
【对标】行为级 FULL + 体感 + 纵深 · ≠像素 · ≠备案完成
【正式上线话术】运维/公网事实；产品对标=行为交付已收，非上线扩权
```



公网入口、Chat 链、下载基址：**以仓库 README / PIN 当前值为准**（asyncova 边缘）；改入口须回写，**不得** 把换域名当对标进度。

---

## 7. 新窗开场报告模板（约 12 行 · 先贴再干）

```text
【交接确认】Aivia Workbench 新窗
真源: HANDOFF + CANON（MEMORY-RESET）
宏观: 通用任务台 · 对标 WorkBuddy · 什么都能干
教育: 仅需真数时 edu-core 只读 · 非主线
作废: 教育专家站主线 · 运维CLAIM=对标 · 备案主线
底盘: Dify+DS+/dl 保留
已收: CLAIM-GENERAL-WB · S3-UX · S4-CAP FULL（S4.1）
下一刀: 维护态 / 业主点名
禁: 空成功 · 写库 · 拆闭源 · 无图假 CLAIM
Chat: https://asyncova.com/chat/lOMVPbz7rZmbJSJl
experts: https://asyncova.com/experts
```



---

## 8. 关联索引

| 文件 | 用途 |
|------|------|
| [docs/CANON.md](./CANON.md) | 唯一正本 |
| [docs/MEMORY-RESET.md](./MEMORY-RESET.md) | 清源公告 |
| [ops/SUPERSEDED.md](../ops/SUPERSEDED.md) | 旧卡作废表 |
| [ops/TASK-CARD-GENERAL-WB.md](../ops/TASK-CARD-GENERAL-WB.md) | 现行主卡 |
| [ops/TASK-CARD-S1-GENERAL-WB.md](../ops/TASK-CARD-S1-GENERAL-WB.md) | S1 子卡（已收） |
| [ops/S1-GENERAL-WB-REPORT.md](../ops/S1-GENERAL-WB-REPORT.md) | S1 报告 |
| [ops/PHASE-GENERAL-WB-PACK.md](../ops/PHASE-GENERAL-WB-PACK.md) | 包 |
| [ops/WB-FEATURE-MATRIX.md](../ops/WB-FEATURE-MATRIX.md) | 通用能力参考（勿收成教育） |
| [README.md](../README.md) | 对外一页纸 |

---

## 9. 交接点名一句

> 业主要的是 **通用能力的 WorkBuddy 级干活台**；  
> 教育是插头（edu-core），不是整栋楼；  
> 前面偏航已清源；S1 已把默认入口改成通用 Agent 并绿了 Word/Excel/短答；  
> S1–S4 已收（能力 + 体感 + 纵深）；新窗 **维护态** 或业主新主线。
