# 调查 · QUAD 上线后修复（深度审查残留）

```
DATE: 2026-08-06
STATUS: BINDING · 修复前必读
前提: CLAIM-QUAD-LAUNCH=YES · 正式上线=是（受限） · FULL-REAL=NO
公网: https://asyncova.com
```

## 审查已确认问题

| ID | 问题 | 严重度 | 目标 |
|----|------|--------|------|
| **F1** | `https://asyncova.com/experts`（无尾 `/`）**302 → `:8443/experts/`**，8443 外网不通 | **P0 阻断体验** | 无尾斜杠也 200 专家页；**禁止**跳到 :8443 |
| **F2** | 边缘依赖 SSH 反向隧道 nohup，无 systemd/探活 | **P0 运维** | systemd（或等价）保活 + 探活失败可察觉 |
| **F3** | 包内约定 `catalog.yaml` / DEPLOY-NOTES 缺失 | **P1 形式+回滚** | 配置进仓 + 部署/回滚 NOTES |
| **F4** | CHECKLIST/AUTH 文件名与包不完全一致 | **P2** | 对齐或交叉链接 |
| **F5** | 客户端矩阵证据偏 curl schannel | **P2** | 补 1 次真浏览器打开专家台+Chat 证据（可截图） |
| **F6** | `workbench.aivia.asia` 大陆 ICP 债 / 品牌双域 | **后置说明** | 本包只写清话术与入口，不强制备案完成 |
| **F7** | full real | **后置** | **不做**；保持 FULL-REAL=NO |

## 不做本包

- edu live full real  
- 全校推广升级  
- WorkBuddy 像素抄  
- 备案流程本身（可写下一步）  

## 验收总原则

修复后 **默认老师路径**（复制 README 链接、不手加斜杠）必须可用；部署可回滚；证据进 `ops/evidence/quad-fix-deploy/`。
