# WorkBuddy 业务组织关系（本机）

```
DATE: 2026-08-06
来源: local-UI + sessions.json + artifact-index + SQLite 字段旁证 + 企业版公开文（Admin）
```

## 1. 核心对象树（用户侧）

```text
User (账号 pom / userId UUID)
│
├── Desktop Shell (Electron 主窗)
│   ├── Nav: 新建任务 | 助理 | 项目 | 专家·技能·连接器 | 自动化 | 更多
│   └── Preferences / 权限默认 / 模型 Auto
│
├── Workspace / 空间
│   └── path 绑定（任务级 workDir 常为 WorkBuddy\<timestamp>）
│
├── Project（项目）
│   ├── 动态
│   ├── 计划（待开始/进行中/已暂停）
│   ├── 任务（聚合会话）
│   ├── 资产（文件/文件夹）
│   └── 右轨绑定: 指令 · 连接器 · 专家 · 技能 · 自动化
│
├── Task / Session (conversationId)
│   ├── status: completed / …
│   ├── mode: craft | ask | …（模板侧）
│   ├── model: auto → 实际模型
│   ├── permission_mode
│   ├── use_sandbox_cli
│   ├── workDir (cwd)
│   ├── Transcript (jsonl: user|reasoning|function_call|tool_result|assistant)
│   ├── ToolCalls (Write, present_files, …)
│   └── Artifacts[]
│         ├── file-changes (diff)
│         └── media (PresentFiles)
│
├── Capability
│   ├── Expert（专家/专家团）
│   ├── Skill（内置 + 可安装）
│   └── Connector（实例态 connected/disconnected）
│
└── Automation
      ├── 定义: prompt, rrule/间隔/单次, model, skills, connectors, 推送
      ├── Runs
      └── Delivery outbox（如微信通道）
```

## 2. 从属关系（一句话）

| 关系 | 说明 |
|------|------|
| User 1—N Session | 侧栏任务列表 |
| Session 1—1 workDir | 每任务时间戳目录（本机样本） |
| Session 1—N ToolCall | 工具循环 |
| Session 1—N Artifact | 索引落盘，可在结果栏打开 |
| Project 1—N Session | 项目任务 Tab 聚合 |
| Project N—N Capability | 右轨绑定专家/技能/连接器/自动化 |
| ComposerDraft → Session | 发送时固化绑定 |
| Automation → 定时产生 Run/Session | 后台；本机 automations 曾 0 行 |

## 3. 前台 vs 后台配置落点

| 配置项 | 用户前台 | 管理/企业后台 | 本机观察 |
|--------|----------|---------------|----------|
| 发任务、选场景、+菜单绑定 | ✅ | | UI 截图 |
| 模型 Auto/列表 | ✅ Composer | 企业可管模型资源 | Auto 可见 |
| 默认权限/完全访问 | ✅ Composer 底栏 | 策略可企业下发 | 底栏可见 |
| 技能安装/连接器认证 | 能力中心部分 | 治理上下架 | 插件 enabled 在 settings |
| 自动化调度 | 自动化页 | 审计/禁用 | 入口在侧栏；本机 0 条定义 |
| 组织成员/角色/停用 | | ✅ Admin | **本机无企业 Admin 屏** |
| 用量/配额/成本归集 | 个人 Credits 可见性 | ✅ 部门归集 | 公开企业文 |
| 审计日志 | | ✅ | 公开企业文 |
| 数字员工 7×24 发布 | 使用侧 | ✅ 创建发布治理 | 公开企业文 |

## 4. 权限边界（本机）

```text
默认: 工作区 cwd allowlist（file-service）
可选: sandbox-cli + sandbox-core 规则
升权: permission_mode / UI「完全访问」
MCP: 本地 proxy 需鉴权（曾 401）
禁: 调查未做逃逸对抗；Aivia 不得复制 bypass 当默认
```

## 5. 与 Aivia 对象映射（clean-room）

| WB | Aivia 拟对象 | 落点 |
|----|--------------|------|
| Session/Task | Dify Conversation + 未来 Task 账本 | Chat |
| workDir + Artifact | bridge `/dl` Artifact | bridge |
| Project | （无）校级项目二期 | Admin |
| Expert/Skill | 多应用 / skills/ 文档 | Console + Admin |
| Connector | edu 只读 + 白名单工具 | bridge + Admin |
| Automation | 定时任务（后置） | Admin |
| Enterprise Admin | Dify 成员 + 自建 ops 看板 | Admin |
| Credits | 用量/配额 | Admin 优先 |

## 6. 组织原则（给 Aivia 实现卡）

1. **老师 Chat 只碰：** 任务对话、推荐、出件、改稿、拒越权。  
2. **能力绑定对象** 与 **治理对象** 分离；禁止把 RBAC/配额按钮堆进 Chat。  
3. **Artifact 必须可定位**（URL 或路径），禁止空成功。  
4. **Workspace 边界** Web 用租户/会话隔离替代本地盘。
