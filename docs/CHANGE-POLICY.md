# 改什么 / 不改什么

```
UPDATED: 2026-08-05 · 主线 Dify Web；OpenWork = 二期再动
```

## 不改（冻结）

1. **乱 fork / 重写 Dify 核**或无必要大改 Agent 框架  
2. 为「更像 WB 像素」的大 UI 重写  
3. 腾讯文档引擎 / 闭源连接器复刻  
4. 把 **OpenWork 桌面** mixed 进主入口或与 Dify 双主线  
5. Agent **直写** edu 业务库  

## 改（优先配置 / 应用 / 工作流）

| 优先级 | 项 | 方式 |
|--------|-----|------|
| P0 | DeepSeek 默认 | Dify 模型供应商 / env |
| P0 | 金路径与空成功清零 | 应用提示 + 工作流强制出件 + 规则 |
| P1 | 课件/教案应用或工作流 | Dify 应用 + 本仓模板资产 |
| P1 | 中心知识库/模板 | Dify 知识库（平台治理） |
| P1 | 超时/步数/配额 | Dify 配置 |
| P1 | 品牌文案 | 站点/应用名 |
| P2 | edu 身份 | `bridge/` |
| P2 | edu 只读/提案 | 工具包装 |
| P3 | OnlyOffice 等精修 | 后置可选 |
| P3 | OpenWork 本地增强 | **二期**，见 `ops/INSTALL-OPENWORK-optional.md` |

## 禁止

- 提交密钥  
- 与 pico 双主线并行开大功能  
- 无 PIN 跟踪的上游大爆炸改核  
- 主文档把 OpenWork 写成默认基线  
