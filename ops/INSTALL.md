# 安装（阶段 A）· 本机可执行包

> 目标：新人按本文 **1h 内** 打开 OpenWork → 配 DeepSeek → 跑通 G0/G0b/G1。  
> 禁止：把密钥提交进仓；宣称成功但无磁盘文件。

## 0. 前置

| 项 | 要求 |
|----|------|
| 系统 | **Windows 优先**；macOS / Linux 亦可 |
| 账号 | DeepSeek 开放平台 API Key（[platform.deepseek.com](https://platform.deepseek.com)） |
| 网络 | 能访问 api.deepseek.com 与 GitHub releases |
| 磁盘 | 预留工作区目录（例如 `D:\\aivia-workspace` 或 `~/aivia-workspace`） |

## 1. 安装 OpenWork（桌面成品）

1. 打开上游 Releases：https://github.com/different-ai/openwork/releases  
2. 取 **最新稳定**（撰写时参考 v0.18.x；以页面最新 public 为准）  
3. 按平台下载安装：
   - **Windows**：对应 `.exe` / installer（若提示未签名，属上游临时状态，确认来源为不同-ai/openwork 官方 release 后安装）
   - **macOS**：`.dmg` / 对应 darwin 包
   - **Linux**：AppImage / deb / rpm / AUR（以 release 资产名为准）
4. 启动应用 → 应进入主界面（**G0 通过标准**）

### 备选：从源码 / CLI（排障用，非默认）

```bash
# 需要 Node + pnpm；桌面另需 Rust/Tauri 工具链
git clone https://github.com/different-ai/openwork.git
cd openwork
pnpm install
pnpm dev          # 桌面
# 或 pnpm dev:web # 仅 Web UI
```

Headless 主机（无 GUI 时参考）：

```bash
npm install -g openwork-orchestrator
openwork start --workspace /path/to/workspace --approval auto
```

## 2. 配置 DeepSeek（G0b）

OpenWork 内嵌 **OpenCode**。DeepSeek 为默认模型（BYOK）。

### 推荐路径（TUI / 应用内）

1. 打开 OpenWork，进入可输入指令的会话（或本机已装的 `opencode` CLI）
2. 输入 `/connect` → 选择 **DeepSeek**（或输入 `deepseek`）
3. 粘贴 API Key（仅存本机，例如 `~/.local/share/opencode/auth.json`；**禁止进 git**）
4. `/models` → 选当前官方推荐模型（如 `deepseek-v4-pro` / 文档写明的默认 chat 模型）
5. 短聊验证：**只回：好** → 应收到「好」（**G0b**）

### 配置文件备选（`opencode.json`）

复制本仓样例：

- `ops/deepseek.env.example` → 本地 `.env`（不提交）
- `ops/opencode-deepseek.json.example` → 合并进项目或用户级 `opencode.json`

要点：

- Provider id 与 credential 中的 id **必须一致**（常用 `deepseek`）
- OpenAI 兼容 base：`https://api.deepseek.com` 或 `https://api.deepseek.com/v1`（以上游当前文档为准）
- 模型 id 以 DeepSeek 开放平台与 OpenCode 内置列表为准，勿写死过期别名

## 3. 本仓与工作区

```bash
git clone https://github.com/juanwan99/aivia-workbench.git
# 在 OpenWork 中「添加本地工作区」指向你的工作目录
# 可将本仓 skills/ 按 OpenWork Skills 管理器导入，或复制到工作区 .opencode/skills/
```

阅读：

- `docs/PROJECT-PLAN.md`
- `docs/GOLD-PATHS.md`
- `ops/G-PATH-RUNBOOK.md`（逐步勾选）

## 4. 金路径顺序（必须）

| 顺序 | ID | 动作 | 通过 |
|------|-----|------|------|
| 1 | G0 | 安装并打开 | 主界面可用 |
| 2 | G0b | DeepSeek 短聊「只回：好」 | 回复正确 |
| 3 | **G1** | 「在工作区写 hello.txt，内容 hi」 | **磁盘有文件且内容为 hi** |
| 4 | G2 | 多轮要生物豌豆杂交 HTML | **有 .html 可打开** |
| 5 | G3 | 运行中停止（若支持） | 停止后不继续写盘 |
| 6 | G4 | 故意失败/中断要文件 | **不得显示成功无文件** |

**G1 未绿：禁止宣称阶段 A 完成，禁止开阶段 B 落地。**

## 5. 回写（强制）

成功后：

1. 填写 `upstream/PIN.md`（OpenWork tag/commit、OpenCode 版本、系统、日期）
2. 在 Issue [#1](https://github.com/juanwan99/aivia-workbench/issues/1) 贴金路径记录（模板见 `docs/GOLD-PATHS.md`）
3. 截图或路径证据：工作区 `hello.txt` 真实存在

## 6. 阶段 B 资产（本包已预备，G1 绿后启用）

| 资产 | 路径 | 用途 |
|------|------|------|
| 交付规则 | `docs/DELIVERY-RULES.md` | R1–R8 落地说明 |
| 课件 Skill | `skills/courseware-html/` | HTML 课件 |
| 教案 Skill | `skills/lesson-plan-docx/` | DOCX 骨架 |
| 限流备注 | `docs/DELIVERY-RULES.md` §配额 | 超时/步数配置入口 |

导入方式：OpenWork → Skills 管理器 → 导入本地文件夹；或复制到工作区 `.opencode/skills/<name>/`。
