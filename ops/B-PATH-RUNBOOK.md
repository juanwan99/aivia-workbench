# 阶段 B 执行清单（纪律 · 10 次电池）

日期：2026-08-05    执行人：phase-b-run（ECS）  
工作台 URL：`https://workbench.aivia.asia`  
Dify pin：`1.16.1`    DeepSeek：`deepseek-chat`  
默认应用名：`Aivia 课件`（advanced-chat / Chatflow）  
证书无警告：否（临时自签）    公网可达：是（内网/控制台验收；外网证书警告）  

正文：`ops/PHASE-B-PACK.md`

## B0 开场

- [x] 能打开入口并登录  
- [x] 打开默认课件应用  
- [x] G1 回归一次可下载  
- [x] **G4** 反空成功一次  
- **B0 结果：** PASS  

## B1 运行时纪律

- [x] System Prompt 已含强制出件 / 禁假绿（见 PACK）  
- [x] （推荐） Workflow 末节点出文件（Chatflow：Start→LLM→Answer 已发布；强制完整代码块出件）  
- [x] 掐失败路径不显示成功（G4）  
- **B1 结果：** PASS  

## B2 双能力

- [x] HTML 课件一句话可下载  
- [x] 教案可下载（格式：Markdown `.md`）  
- [x] 同会话改稿仍有文件（T2/T6）  
- **B2 结果：** PASS  

## B3 配额

- [x] 超时/限额已配置（数字记 Issue）  
- [x] 触发一次人话提示（G4 失败人话）  
- **B3 结果：** PASS（起点：LLM `max_tokens=8192`、`temperature=0.3`；工作空间日配额待试点前与业主定最终数字）  

## B4 品牌（可选）

- [x] 完成（应用名 Aivia 课件 + 欢迎语）  

## B5 平台模板/知识库

- [x] 知识库或模板骨架已挂（`Aivia课件结构模板` economy + 结构文档）  
- [x] 不自建库也能出结构完整课件（系统提示固化结构）  
- **B5 结果：** PASS  

## 10 次电池（空成功必须 0）

| # | 话术摘要 | 要文件? | 产物文件名 | 结果 |
|---|----------|---------|------------|------|
| T1 | 豌豆杂交 HTML | 是 | t1-artifact.html | PASS |
| T2 | 同会话加练习 | 是 | t2-artifact.html | PASS |
| T3 | 二次函数 HTML | 是 | t3-artifact.html | PASS |
| T4 | 《背影》教案 | 是 | t4-artifact.md | PASS |
| T5 | 水的三态 HTML | 是 | t5-artifact.html | PASS |
| T6 | 同会话改目标导出 | 是 | t6-artifact.html | PASS |
| T7 | 只要大纲 | 否 | — | PASS |
| T8 | 一般现在时 HTML | 是 | t8-artifact.html | PASS |
| T9 | 「课件」二字 | 是* | t9-rerun.html | PASS（首轮 FAIL 后修 prompt 重跑） |
| T10 | 施压不假绿 | 是 | t10-artifact.html | PASS |

空成功次数：**0**  
质量抽检 ≥3 个文件：**PASS**（8/8 HTML 可打开/有标题/非半截）  

## 回写

- [x] Issue #1 结果评论（无密钥）  
- [x] PIN 补 B 出口一行  
- [x] 仅当空成功=0 才勾 PLAN M3  

```text
摘要：
日期: 2026-08-05
空成功数: 0
B0–B5: 全 PASS
证书/可达: 自签证书有警告；控制台与业务可验收
备注: 默认入口 Chatflow 公开 https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl ；产物目录 /home/ops/aivia-phase-b-artifacts/
```
