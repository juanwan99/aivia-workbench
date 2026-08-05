# Aivia Workbench · 项目总规划 v0.7

```
STATUS: BINDING · 2026-08-06
BASE: Dify Web · DeepSeek · edu bridge mock
UPDATED: CLAIM-D-LITE 绿；E1 后置；CLAIM-B 否；正式上线否
```

## 1. 产品

打开域名 → 登录 → 任务 → **可一键下载产物** → 诚实状态。  
对标 WorkBuddy **行为**，不抄 UI。  
C：租户身份 + 只读 + 提案人审（mock 绿）。  
D-LITE：受控轻量内测（非正式上线）。

## 2. 阶段

### A · 跑通 — 功能绿
### B · 纪律 — 电池有条件绿
### B-HARDEN — 应用硬化绿
### DEBT-CLEAR — 应用侧绿 · E1 后置
### C · edu 桥 — **CLAIM-C 绿（MODE=mock）**
### C-FIX-DEPLOY — **CLAIM-C-FIX 绿**
### D-LITE · 轻量内测 — **CLAIM-D-LITE 绿**（≠ 正式上线）
### D · 全量试点（M5）— **E1 绿后**

## 3. 里程碑

- [x] M0–M2 功能  
- [x] M3 纪律电池（有条件）  
- [x] M3b 应用硬化  
- [ ] M2b/H2/E1 正式 HTTPS（后置）  
- [x] M4 edu 桥（mock 契约绿；real 后置）  
- [x] M4b 轻量内测（CLAIM-D-LITE）  
- [ ] M5 全量试点（绑 E1 + 扩教师授权）  

## 4. 近期下一刀

1. **E1 DNS-01**（业主 · 优先）→ 解 CLAIM-B 门  
2. 接 edu-core real 只读白名单（回归 Ce2–Ce5）  
3. Dify 控制台挂载 `bridge/openapi.json` 自定义工具（可选增强）  
