# Aivia Workbench · 项目总规划 v0.6

```
STATUS: BINDING · 2026-08-05
BASE: Dify Web · DeepSeek · edu bridge mock
UPDATED: CLAIM-C 绿(mock)；E1 后置；CLAIM-B 否
```

## 1. 产品

打开域名 → 登录 → 任务 → **可一键下载产物** → 诚实状态。  
对标 WorkBuddy **行为**，不抄 UI。  
C：租户身份 + 只读 + 提案人审。

## 2. 阶段

### A · 跑通 — 功能绿
### B · 纪律 — 电池有条件绿
### B-HARDEN — 应用硬化绿
### DEBT-CLEAR — 应用侧绿 · E1 后置
### C · edu 桥 — **CLAIM-C 绿（MODE=mock）**
### D · 试点 — E1 绿后

## 3. 里程碑

- [x] M0–M2 功能  
- [x] M3 纪律电池（有条件）  
- [x] M3b 应用硬化  
- [ ] M2b/H2/E1 正式 HTTPS（后置）  
- [x] M4 edu 桥（mock 契约绿；real 后置）  
- [ ] M5 试点  

## 4. 近期下一刀

1. 接 edu-core real 只读白名单（回归 Ce2–Ce5）  
2. E1 DNS-01（业主）  
3. Dify 控制台挂载 `bridge/openapi.json` 自定义工具（可选增强）  
