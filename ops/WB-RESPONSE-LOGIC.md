# WorkBuddy 响应逻辑（本机行为剧本）

```
DATE: 2026-08-06
来源: local-UI + 本机 transcript/artifact（非广告语）
App: 5.3.5
```

## 状态机（文字）

```text
空闲(Idle)
  │ 用户: 新建任务 / 选场景 chip / 填 Composer / 发送
  ▼
受理(Accepted) —— 分配 conversationId + workDir(WorkBuddy\<ts>)
  │ 注入: user_info / workspace / identity 文件 / connector-status / 权限模式
  ▼
推理(Reasoning) —— model=auto→实际模型；可有短 reasoning
  │
  ├─► 工具循环(ToolLoop) —— function_call → function_call_result → …
  │     例: Write → present_files
  │
  ▼
交付(Delivered) —— 助手文本 + artifact-index(file-changes|media)
  │
  ├─► 完成(Completed) —— 可投影耗时/消耗/模型
  └─► 失败(Failed) —— 人话错误（本机样本未强制失败用例）

可选分支:
  停止 → Cancelled（UI 应保留已停止语义）
  只要短答 → 可无工具、无文件产物
```

## 剧本 R1 · 工作区写文件（真会话）

| 步 | 时序 | 观察 |
|----|------|------|
| 1 | 用户侧栏「新建任务」或发指令 | Menu/入口 → 新 session |
| 2 | 指令 | 「在工作区写一个 hello.txt，内容为 hi」 |
| 3 | 系统 | `workDir=…\WorkBuddy\2026-07-30-06-45-08` · `sessionId=70e9bab6-…` |
| 4 | 注入 | identity（SOUL/IDENTITY/USER/BOOTSTRAP）· connector-status 大列表 · permission 模式 |
| 5 | 模型 | `requestModelId=auto` → **实际 `glm-5.2`** · agent=`cli` |
| 6 | 工具1 | `Write(hello.txt, hi)` → Successfully created… |
| 7 | 工具2 | `present_files([hello.txt])` → present_files_result |
| 8 | 交付 | 助手说明路径与内容；**artifact-index** 写入 file-changes + media(PresentFiles) |
| 9 | 终态 | 文件 2B 在 cwd；任务列表可见标题 |

**证据：**  
- transcript: `~\.workbuddy\projects\…\70e9bab6-….jsonl`  
- artifact: `~\.workbuddy\artifact-index\70e9bab6-….json`  
- 文件: `~\WorkBuddy\2026-07-30-06-45-08\hello.txt`  

**结论：** 非「纯聊天一次返回」；是 **工具循环 + 工作区写盘 + 产物索引**。

## 剧本 R2 · 纯问答（1+1）

| 步 | 观察 |
|----|------|
| 用户 | 「测试1+1等于几」类（多条历史） |
| 系统 | 仍建 workDir + session；mode 历史为 craft / permission bypass 见账本 |
| 模型 | auto→glm-5.2 |
| 工具 | **本样本未见 Write**；直接 assistant 文本（约「1+1=2」） |
| 产物 | 无强制文件 |

**证据：** 任务列表 UI 可见多条「测试1+1…」；transcript `7d1ce05e-…` / `b2bbe2bf-…` 有 output_text 无文件工具。  

**结论：** 短答路径 **可以不硬塞文件**（对照 Aivia G3/S4）。

## 剧本 R3 · 场景 chip 改变能力上下文

| 步 | 观察 |
|----|------|
| 首页 | 三场景 Tab：日常办公 / 代码开发 / 设计创意 |
| 点「设计创意」下某 chip | Composer 出现**可移除能力标签**；建议文案切换；出现「相关灵感」卡片区 |
| 非行为 | 不仅是把模板句塞进 textarea |

**证据：** `wb-home-design-chip-selected.png` + 可访问性树。  

**结论：** 场景 = **结构化能力选择**，不是推荐文案玩具。

## 剧本 R4 · Composer「+」组合绑定

| 步 | 观察 |
|----|------|
| 点 Composer 左下 `+` | 弹出：添加文件 / 模式 / 专家 / 技能 / 连接器（均有子级箭头） |
| 语义 | 每一项对应不同输入对象，进入后续任务绑定 |

**证据：** `wb-composer-add-menu.png` / `.txt`。  

**结论：** 任务输入是 **多对象草稿**，不是单文本框。

## 剧本 R5 · 产物呈现路径

| 步 | 观察 |
|----|------|
| 写盘成功后 | `present_files` 工具 |
| 索引 | artifact `type=media` + `file-changes`（含 diff） |
| UI 结果栏 | 对齐调查：工作空间文件树可非空；概览/浏览器分栏 |

**结论：** 交付闭环 = **工具写盘 → Present → 结果栏可打开**，不是仅 Markdown 代码块。

## 剧本 R6 · 权限与沙箱（旁证）

| 观察 | 来源 |
|------|------|
| 会话 `permission_mode` 可为 bypassPermissions | 历史 session 日志 |
| UI「默认权限」下拉 | home Composer 底栏 |
| sandbox-core：cwd allowlist、sessions GC | `~\.workbuddy\logs\sandbox\*` |
| file-service 读目录限当前 workDir | cleanroom 笔记 |

**结论：** 默认有边界；高权限模式可放宽——Aivia 应对齐 **默认紧、显式升权**。

## 与 Aivia 响应逻辑对照

| 点 | WorkBuddy | Aivia 现行 |
|----|-----------|------------|
| 任务化 | session+cwd+工具循环 | Dify 会话 + Chatflow |
| 出件 | Write+Present+本地路径 | PackDownload → https `/dl` |
| 无文件短答 | 可 | S4/G3 已绿 |
| 改稿 | 同 cwd 多轮工具 | 同会话新 `/dl`（S5） |
| 过程可见 | reasoning+tool+结果栏 | 流式文本为主 |
| 停止 | UI 停止控件 | Dify 停止，cancelled 语义弱 |
| 失败人话 | 产品化 | R8 / S6 拒写库 |

## 未在本机用实时新任务证实（诚实）

- 复杂多步 Plan 面板是否稳定出现  
- 自动化定时触发一条完整 run  
- 企业 Admin 审批流  
- 失败自动重试策略  

（不阻塞 CLAIM；已在组织/矩阵标【未实时】）
