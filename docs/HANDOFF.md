# HANDOFF · Aivia Workbench 总管交接

```
DOC: docs/HANDOFF.md
DATE: 2026-08-05
STATUS: BINDING · 新窗唯一入口（开场先读 docs/CANON.md）
UPDATED: 2026-08-05 · A 功能绿 · B 纪律电池有条件绿 · 下一刀 = PHASE-B-HARDEN
```

---

## 0. 你是谁 · 怎么接

1. 先读 [`docs/CANON.md`](./CANON.md) + 本文 + [`ops/PHASE-B-CLOSEOUT.md`](../ops/PHASE-B-CLOSEOUT.md) + [`ops/PHASE-B-HARDEN-PACK.md`](../ops/PHASE-B-HARDEN-PACK.md)  
2. 按 §5 打约 15 行状态再干活  
3. 真源：主仓 aivia-workbench · 上游 Dify · pico 冻结  
4. 禁止：密钥进仓、自 PASS、空成功、OpenWork 主线、未授权 C、未 Harden 宣称教师正式可用  

---

## 1. 北极星

浏览器打开域名 → 登录 → 任务 → **可下载产物** → 停/重试 → 状态诚实。  
模型 DeepSeek。对标 WorkBuddy **行为** clean-room。

---

## 2. 主线决策（BINDING）

Dify Web + DeepSeek + 现网；OpenWork 二期；edu 后置不写库；不乱 fork Dify 核。

---

## 3.1 入口

| 项 | 状态 |
|----|------|
| 主站 | `https://workbench.aivia.asia` |
| **默认应用** | `https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl`（Aivia 课件 Chatflow） |
| 证书 | 自签 → Harden H2 |
| 公网 | 有 403 隐患 → H2 |

---

## 4. 文档地图

| 路径 | 用途 |
|------|------|
| CANON | 正本 |
| PHASE-B-CLOSEOUT | B 有条件收口 |
| PHASE-B-HARDEN-PACK | **当前执行包** |
| B-HARDEN-RUNBOOK | 勾选 |
| PHASE-A-CLOSEOUT | 证书/WAF 同源 |
| PIN | 版本与出口 |
| PHASE-B-PACK | B 电池历史包（已跑） |

Issue：https://github.com/juanwan99/aivia-workbench/issues/1  

---

## 5. 状态报告模板

```text
【状态】Aivia Workbench 交接后首报
主仓: juanwan99/aivia-workbench @ <sha>
正本: Dify Web + DeepSeek + 现网
Pin: Dify 1.16.1 · deepseek-chat
入口: workbench · 默认 chat/lOMVPbz7rZmbJSJl
阶段: A 功能绿 | B 纪律电池有条件绿（空成功0）| B 硬化 OPEN
下一刀: PHASE-B-HARDEN（H1真下载 H2证书/公网 H3真配额 H4教案 H5单入口 H7回归）
阻塞: <证书/WAF/配额数字…>
不做什么: 重做B电池大叙事、OpenWork主线、未授权C、假正式上线
```

---

## 6. 当前进度

| 项 | 状态 |
|----|------|
| A G0–G1+ | **PASS** |
| B 10 次空成功 0 | **PASS**（有条件 M3） |
| B3 真配额 | **PARTIAL** |
| 交付=平台下载 | **OPEN** H1 |
| 正式 HTTPS / 公网 | **OPEN** H2 |
| 阶段 C edu | **未做** 须授权 |
| OpenWork | 二期 |

**下一刀（唯一主线）：** `ops/PHASE-B-HARDEN-PACK.md`  

---

## 7. 阶段速查

| 阶段 | 状态 |
|------|------|
| A | 功能绿；入口跟 Harden |
| B | 电池有条件绿；**硬化中** |
| C | 授权后 |
| D | 试点后 |

---

## 11. 行动令

```text
1) 读 CANON + B-CLOSEOUT + B-HARDEN-PACK
2) §5 状态报告
3) 执行 H0–H7，勾 B-HARDEN-RUNBOOK
4) 回写 Issue #1 + PIN
5) Harden 绿且 H2 过后再谈对外；C 须授权
```
