# WB-SURVEY 引用源（local-UI 优先 · web 补充）

```
DATE: 2026-08-06
PHASE: PHASE-WB-SURVEY
权重: local-UI / 本机会话 > web 公开文
```

## A. local-UI / 本机（主）

| # | 源 | 类型 | 用途 |
|---|-----|------|------|
| L-UI-01 | `ops/evidence/wb-survey/ui/wb-home-office.png` + `.txt` | 截图+可访问性树 | 主壳、导航、办公场景、任务列表 |
| L-UI-02 | `ui/wb-home-code.png` + `.txt` | 同上 | 代码开发场景建议 |
| L-UI-03 | `ui/wb-home-design.png` + `.txt` | 同上 | 设计创意场景 |
| L-UI-04 | `ui/wb-home-design-chip-selected.png` + `.txt` | 同上 | chip 结构化标签+灵感 |
| L-UI-05 | `ui/wb-composer-add-menu.png` + `.txt` | 同上 | + 菜单五类绑定 |
| L-UI-06 | `ui/README.md` | 索引 | D0 环境与覆盖表 |
| L-SESS-01 | `~\.workbuddy\projects\…\70e9bab6-….jsonl` + artifact-index + `WorkBuddy\…\hello.txt` | 本机会话 | 写文件工具循环剧本 |
| L-SESS-02 | 同目录其它 1+1 会话 jsonl | 本机会话 | 纯问答无强制文件 |
| L-CFG-01 | `~\.workbuddy\app\sessions.json` · `window-state.json` · `last-launch.json` | 配置结构 | 版本/会话绑定/窗尺寸 |
| L-CFG-02 | `~\.workbuddy\settings.json`（仅结构：sandbox/claw/enabledPlugins 键名） | 配置结构 | 插件与通道开关形态；**无密钥值进仓** |
| L-FS-01 | 安装目录 `builtin-skills` / `templates` **目录名列表** | 可见资源名 | 技能与模式模板名 |
| L-LOG-01 | `~\.workbuddy\logs\sandbox\*` · CliDispatcher 行 | 日志摘要 | 沙箱路径、permissionMode |
| L-NOTE-01 | `~/WorkBuddy-cleanroom-architecture.md`（2026-08-05） | 架构笔记 | 进程/端口/对象边界旁证 |

## B. web 公开（补充 · 不得替代本机）

| # | 源 | 用途 |
|---|-----|------|
| W-01 | https://www.workbuddy.cn/ | 定位与生态名 |
| W-02 | https://www.codebuddy.cn/work/ | 多专家/场景文案 |
| W-03 | https://www.pingwest.com/a/314412 | **企业 Admin**：组织、审计、用量、数字员工、Connector、Skills |
| W-04 | https://developer.cloud.tencent.com/article/2658096 | 桌面能力教程交叉 |
| W-05 | https://www.eigent.ai/zh-HK/blog/workbuddy-ai-review | 多代理/MCP 交叉 |
| W-06 | https://www.53ai.com/news/shuziyuangong/2026020601269.html | 模式/技能/连接器操作描述 |

## C. Aivia 现状锚点

| # | 源 | 用途 |
|---|-----|------|
| A-01 | `docs/CANON.md` · `upstream/PIN.md` | 主线 CLAIM |
| A-02 | `ops/SCENE-FULL-REPORT.md` · evidence/scene-full | 个人全场景 P0 |
| A-03 | `ops/DOC-SOLID-REPORT.md` · `ops/DL-FIX-REPORT.md` | 真文件 · https /dl |
| A-04 | `bridge/README.md` | hybrid · 拒写库 |
| A-05 | `docs/RESPONSE-LOGIC.md` · DELIVERY-RULES | R1–R8 |
| A-06 | Dify 1.16.1 控制台（应用/成员/知识库） | 管理员「部分」锚点 |

## 纪律

- 矩阵「来源」列优先 `L-*`；企业 Admin 细项可标 `W-03` 并备注 **非本机 Admin 实测**。  
- **网搜-only 条目不得构成矩阵主体。**  
- 不贴 Cookie、Token、账号密码、个人文件正文（hello 内容 `hi` 为例外已公开测试）。
