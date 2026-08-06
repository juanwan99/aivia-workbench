# WB-SURVEY 报告（本机深查 · 仅调查）

```
DATE: 2026-08-06
PHASE-WB-SURVEY: DONE
CLAIM-WB-SURVEY: YES
深查: 本机 UI + 响应逻辑 + 业务组织 + 矩阵
矩阵: 48 条 · G=17
证据: ops/evidence/wb-survey/
开发: 否 · 正式上线: 否 · 1:1 对齐: 否
```

## 1. 结论

以本机 WorkBuddy **5.3.5** 为准：产品是 **Electron 任务工作台**（侧栏六入口 + 组合 Composer + 工具循环写盘 + 结果栏产物），不是单页聊天壳。  
Aivia 现行 Web 在 **个人交付 P0**（课件/教案/表/大纲/改稿/拒写库/`/dl`）已可用；差距集中在 **组合输入与结果栏对象、项目/专家/自动化壳、厚管理员后台**。  
**CLAIM-WB-SURVEY = 深查四件套齐** · **≠** 功能对齐 · **≠** 上线。

## 2. UI / 逻辑 / 组织 差异摘要

| 维 | WorkBuddy（本机） | Aivia 现行 | 含义 |
|----|-------------------|------------|------|
| UI | 六入口壳 · 场景 chip 结构化 · +五类绑定 · 结果栏三视图 | 单 Chat · 推荐问题 · `/dl` 链 | 壳与对象差一截 |
| 响应 | session+cwd+tool loop+PresentFiles | Chatflow+PackDownload | 交付形态不同但可对齐行为 |
| 组织 | User–Project–Session–Artifact–Capability–Automation | Conversation–Artifact(/dl)–（弱管理） | 缺 Project/Capability 绑定账本 |
| 管理 | 企业 Admin 厚（本机个人号未进） | Dify 控制台部分 | G 域多数要自建/运营化 |

详见：`WB-IA.md` · `WB-RESPONSE-LOGIC.md` · `WB-ORG-MODEL.md`。

## 3. Top 缺口 · 用户前台

| # | 拟名 | ID | 建议期 |
|---|------|-----|--------|
| 1 | 组合输入条（文件+技能先） | A-07 | P1 |
| 2 | 产物面板/文件索引 | B-09 | P1 |
| 3 | 场景 chip 结构化（非纯文案） | A-06 加深 | P1 |
| 4 | 上传再加工 | C-01 | P1 |
| 5 | PPT | B-03 | P1 |
| 6 | 工作模式切换 | E-03 | P1 |
| 7 | 运行摘要（耗时/模型） | A-08 | P2 |
| 8 | 桌面工作区 | C-02/H-01 | 后置 |

**禁止：** 把 G 域治理控件堆进老师 Chat。

## 4. Top 缺口 · 管理员后台（业主重点）

| # | 拟名 | ID | 建议期 | 备注 |
|---|------|-----|--------|------|
| 1 | 配额/真日限额 | G-07 | **P0** | |
| 2 | 空成功/失败监控 | G-13 | **P0** | |
| 3 | 审计（会话+下载+工具） | G-03 | **P0** | |
| 4 | 写库门禁策略化 | G-05 | **P0** | |
| 5 | 组织+教育角色 | G-01/02 | P1 | 企业文+Dify 部分 |
| 6 | 用量看板 | G-06 | P1 | |
| 7 | 技能发布流程 | G-10 | P1 | |
| 8 | edu full real | G-12/I-06 | P1 | 另卡 |
| 9 | 连接器策略 | G-04 | P1 | |
| 10 | 自动化治理 | G-16 | P2 | |

落点：**Dify Console + 轻 Admin/ops + bridge**，不复制腾讯 Admin UI。

## 5. 建议三期（只建议 · 本包不开发）

**期 0 守住+可运营：** 回归 SCENE-FULL；实现卡勾 `G-07,G-13,G-03,G-05`。  
**期 1 用户补强+轻管理：** `A-07` 精简、`B-09`、`C-01`、模板；`G-01/06/10/14`。  
**期 2 专家/连接/多端：** `E-*`、`D-03/05`、`H-03`、数字员工。

## 6. 红线

- 逆向拆包 / 密钥进仓 / 网搜-only 充深查  
- 本卡开发冒充调查完 / 宣称已对齐全功能 / 正式上线  
- 全能力塞 Chat / Agent 直写成绩库 / 像素抄 UI  

## 7. CLAIM 核对

| 门禁 | 状态 |
|------|------|
| D1 UI ≥8 类 + WB-IA | YES · ui/ + WB-IA.md |
| D2 ≥5 剧本 + RESPONSE-LOGIC | YES · R1–R6 |
| D3 ORG-MODEL | YES |
| D4 矩阵≥40 G≥12 含入口路径 | YES · 48/G17 |
| D5 REPORT | YES |
| sources local vs web | YES |
| 无开发充数 · 无密钥 | YES |

```text
CLAIM-WB-SURVEY: YES
开发实现: 否
正式上线: 否
```
