# 标准任务卡 · WB-ALIGN（完整 · 无人值守）

```
════════════════════════════════════════════════════════
标准任务卡 · PHASE-WB-ALIGN（单包单卡 · 全流程）
════════════════════════════════════════════════════════
执行窗：本机 Grok（可 SSH 云端改 Dify/nginx/bridge）
        + 本机浏览器 / Excel|WPS|Word 验收
上下文：CLEAR
  CLAIM-WB-SURVEY=YES · MATRIX 为范围真源
  已收 CLAIM-B · DOC-SOLID · DL-FIX · SCENE-FULL
  正式上线=否 · 禁止无表开发
角色：按 WorkBuddy 对标矩阵把 P0+P1 做齐（名字可不同；管理归后台）
模式：分阶段 S0→S5 无人参与；每阶段自审→修复循环→再过门→自动下阶段
RISK: 高（现网配置；限流；日志；勿密钥；勿写库；勿假绿跳阶段）
FAST: 否 · 高标准 · 浏览器验收为准
仓：juanwan99/aivia-workbench
BASE：https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl
下载主路径：https://workbench.aivia.asia/dl/...

【真源】
  ops/PHASE-WB-ALIGN-PACK.md
  ops/WB-ALIGN-RUNBOOK.md
  ops/WB-FEATURE-MATRIX.md
  ops/WB-SURVEY-REPORT.md
  ops/WB-ORG-MODEL.md
  ops/WB-RESPONSE-LOGIC.md
  docs/CANON.md
  本卡

【硬门禁·整包】
  1) 每阶段 gate-S{n}.md 自审 PASS 后才允许进入下一阶段
  2) 任一门 FAIL：本阶段修复（记 fix-log），禁止跳过
  3) 连续修复仍 FAIL：整包 BLOCKED 并回写，禁止假 CLAIM
  4) 终包：WB-ALIGN-REPORT + MATRIX-STATUS + evidence/wb-align/
  5) PIN CLAIM-WB-ALIGN=YES|BLOCKED + CANON + Issue + push
  6) 空成功=0 · 无 data-URL 主路径 · 无 [blocked] · 无密钥进仓

【阶段与验收（摘要·细则见 PACK）】
  S0 底盘回归
     过线: S1/S3/S4/S6/S8 类路径绿 · /dl attachment · 本机打开 · 空成功0
  S1 管理P0（G-03/05/07/13）
     过线: 审计样例 · 写库再拒 · 配额/限流可证 · 空成功监控可证
  S2 用户交付壳（B-07/09 · A-08 · 格式回归）
     过线: 三格式 /dl · 产物可见区 · 状态摘要 · 本机打开
  S3 输入与场景（A-06/07 · C-01/04 · 防串台）
     过线: ≥4 场景入口 · 上传再加工1次 · 模板≥2 · S7 再绿
  S4 矩阵P1 扫尾
     过线: 每一 P0/P1 ID 有「有/等价/跳过+原因」· 无静默空洞
  S5 终回归+回写
     过线: 全回归 · FINAL gate · REPORT · 真源 · Issue

【自审协议】
  每阶段结束复制 PACK §4 模板 → ops/evidence/wb-align/gate-S{n}.md
  自审项全部 PASS 才能写「进入 S{n+1}」
  中途不向业主请示放行；只在整包结束或 BLOCKED 回写

【本地测强制】
  用户路径：浏览器发送 → 点 /dl → 系统应用打开 → 证据进仓
  管理路径：现网可操作配置/日志 + 脱敏 evidence
  禁止仅 API 烟测代替浏览器

【不做】
  拆闭源 · 像素抄 UI · 全能力塞老师 Chat
  桌面控盘/IM 全量未声明却标「有」
  跳阶段 · 空成功报绿 · 假正式上线 · Agent 写成绩库
  无 MATRIX-STATUS 声称全面对齐

【出口】
  CLAIM-WB-ALIGN=YES ⇔ S0–S5+FINAL 全 PASS + 回写齐
  = 高标准对标实现（P0+P1 可验收）
  ≠ WorkBuddy 1:1 复制 ≠ 自动全校上线
  BLOCKED 时诚实写原因与已完成阶段
════════════════════════════════════════════════════════
```
