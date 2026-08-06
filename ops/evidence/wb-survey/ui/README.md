# 本机 WorkBuddy UI 证据索引

```
DATE: 2026-08-06
App: WorkBuddy 5.3.5 (build 8044e898…) · Windows
角色: 个人账号 pom · 本机无企业 Admin 控制台权限
方法: 真机可访问性树/截图（2026-07-30 对齐调查）+ 本机会话 transcript/artifact（2026-07-30）
禁止: 逆向 asar 利用 · 密钥进仓
```

## 环境（D0）

| 项 | 值 |
|----|-----|
| OS | Windows 10/11 |
| 安装 | `%LOCALAPPDATA%\Programs\WorkBuddy\` · winget `Tencent.WorkBuddy` |
| 版本 | **5.3.5**（`last-launch.json`） |
| 用户数据 | `%USERPROFILE%\.workbuddy\` |
| 任务 cwd | `%USERPROFILE%\WorkBuddy\<时间戳>\` |
| 窗口 | 1452×877（`window-state.json`） |
| 冷启动 | 主进程常驻；调查日进程在跑、主窗可能托盘化 → 以已落盘 UI 截图+会话为准 |
| 角色 | **个人**；企业 Admin 后台 **本机未进入**（G 域部分依赖 web 企业版说明交叉，已在 sources 降权标注） |

## 截图 / 可访问性（≥8 类覆盖）

| # | 界面类 | 文件 | 可见要点 |
|---|--------|------|----------|
| 1 | 主壳总览 · 新建任务首页 | `wb-home-office.png` + `.txt` | 顶栏菜单 · 左栏六入口 · 中区标题/场景/Composer · 底栏账号 |
| 2 | 场景：日常办公 | 同上 | chip：文档处理/金融/数据可视化/深度研究/视频/幻灯片 |
| 3 | 场景：代码开发 | `wb-home-code.png` + `.txt` | 不同建议集合（开发向） |
| 4 | 场景：设计创意 | `wb-home-design.png` + `.txt` | 设计向建议 |
| 5 | 场景 chip 选中态 | `wb-home-design-chip-selected.png` + `.txt` | 结构化标签 + 相关灵感区 |
| 6 | Composer「+」菜单 | `wb-composer-add-menu.png` + `.txt` | 添加文件 / 模式 / 专家 / 技能 / 连接器 |
| 7 | 历史任务列表 | home 截图左栏 | 任务(4)：hello.txt、1+1 测试等 |
| 8 | 空间/项目入口 | home 截图 | 空间(1) · 项目新手指引 |
| 9 | 底栏账号/消息/小程序 | home 截图 | pom · 铃铛 · 扫码小程序 |
| 10 | 产物（非截图·落盘） | 本机 `WorkBuddy\2026-07-30-06-45-08\hello.txt` + `artifact-index\…json` | file-changes + PresentFiles media |

## 一级导航（可访问性树 · local-UI）

```
侧栏 Agents tabs:
  新建任务
  助理
  项目
  专家·技能·连接器
  自动化
  更多（资料库·灵感）
任务 (N)  ← 历史会话按钮列表
空间 (N)  ← 项目入口
底栏: 账号 · 消息中心 · 扫码小程序
顶栏: 收起侧栏 · 搜索 · 筛选 · 版本 v5.3.5
```

## 诚实边界

- 本包 **未** 在调查日逐一点开「自动化表单全部字段 / 企业 Admin」实时截图；自动化表结构与日志旁证见 `WB-ORG-MODEL` / cleanroom 笔记。  
- 企业级管理后台（用量归集、组织 RBAC 细项）以 **web 企业版公开文** 补，且在矩阵标 `web` 源，**不冒充本机 Admin 实测**。  
- 未拆包、未贴 Cookie/Token。
