# 安装（阶段 A）· 现网 Dify Web + DeepSeek

> 目标：在**现有服务器**上 Docker 部署 Dify → 配 DeepSeek → 浏览器跑通 G0/G0b/G1。  
> 禁止：密钥提交进仓；宣称成功但无可下载文件。  
> 官方文档（以官网为准）：https://docs.dify.ai （Docker Compose 自托管）

## 0. 前置

| 项 | 要求 |
|----|------|
| 机器 | **沿用现网服务器**（CPU≥2、RAM≥4GiB，官方最低；生产建议更宽裕） |
| 软件 | Docker 19.03+ · Docker Compose **2.24.0+** |
| 账号 | DeepSeek API Key（[platform.deepseek.com](https://platform.deepseek.com)） |
| 域名 | 建议子域如 `workbench.aivia.asia` → 反代到 Dify（见 `ops/INFRA.md`） |
| 网络 | 能拉镜像、访问 api.deepseek.com |

## 1. Docker Compose 安装 Dify（要点）

完整步骤以 **Dify 官方 Self-host / Docker Compose** 为准。摘要：

```bash
# 取官方推荐 tag（示例：跟踪最新 release tag）
git clone --branch "$(curl -s https://api.github.com/repos/langgenius/dify/releases/latest | jq -r .tag_name)" \
  https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
# 按需编辑 .env（端口、密钥、存储等）——真实密钥勿提交本仓
docker compose up -d
docker compose ps   # 核心容器应为 Up/healthy
```

访问（安装后）：

- 初始化管理员：`http://<服务器IP>/install` 或经反代的 `https://workbench.aivia.asia/install`  
- 日常入口：同 Host 根路径  

### 反代 / HTTPS

- 用 Caddy / Nginx / Traefik 将 `workbench.aivia.asia` 转到 Dify 暴露端口（默认常见 80，以 `.env` 为准）  
- 证书：Let’s Encrypt 或现有证书体系  
- **不要**与 `pico.aivia.asia` 抢同一用途；按 Host 分流  

## 2. 配置 DeepSeek（G0b）

1. 登录 Dify 控制台  
2. **设置 → 模型供应商（Model Providers）**  
3. 找到 **DeepSeek**，填入 API Key 并保存  
4. 在应用/对话中选用 DeepSeek 模型（如 `deepseek-chat` / 平台当前推荐名）  
5. 短聊验证：「只回：好」→ 应得到「好」  

环境变量样例（仅服务器本地，不进 Git）：见 `ops/deepseek.env.example`。

## 3. 本仓

```bash
git clone https://github.com/juanwan99/aivia-workbench.git
# 规划与金路径在 docs/、ops/；应用导出可后置放入 skills/ 或独立目录
```

阅读：`docs/GOLD-PATHS.md`、`ops/G-PATH-RUNBOOK.md`、`docs/DELIVERY-RULES.md`。

## 4. 金路径顺序（浏览器）

| 顺序 | ID | 动作 | 通过 |
|------|-----|------|------|
| 1 | G0 | 浏览器打开 URL | 主界面/登录可用 |
| 2 | G0b | DeepSeek 短聊「只回：好」 | 回复正确 |
| 3 | **G1** | 要 HTML 课件并下载 | **有可下载文件** |
| 4 | G4 | 失败场景 | 不假绿无文件 |

**G1 未绿：禁止宣称阶段 A 完成。**

## 5. 回写（强制）

1. `upstream/PIN.md` 填写 **Dify 版本/镜像 tag**、日期、系统  
2. Issue #1 贴金路径记录  
3. 产物：截图或下载文件名证据（无密钥）  

## 6. 二期（非本阶段）

桌面 OpenWork 安装见 [`ops/INSTALL-OPENWORK-optional.md`](./INSTALL-OPENWORK-optional.md)，**不是**当前下一刀。
