# 正本 · CANON（唯一现行口径）

```
DOC: docs/CANON.md
DATE: 2026-08-05
STATUS: BINDING · 与 HANDOFF 同级；冲突时以本文 + HANDOFF 最新 UPDATED 为准
```

## 1. 现行真相（请先背这 8 条）

1. **产品形态：** 浏览器 / 公网 Web 工作台（不是默认桌面客户端）。  
2. **主底座：** **Dify**（自托管 Docker）。  
3. **模型：** **DeepSeek** API。  
4. **部署：** 云端优先，挂**现有服务器 + 域名/IP**（`ops/INFRA.md`）。  
5. **下一刀：** 现网装 Dify → 配 DS → **浏览器 G1**（可下载产物）。  
6. **OpenWork / OpenCode / 桌面：** **二期可选**，不占主入口，禁止与 Dify 双主线。  
7. **edu-core：** 后置身份桥；AI **不**直写业务库。  
8. **交付：** 要文件必须有可下载文件；禁止空成功、禁止自 PASS、禁止密钥进仓。

## 2. 已作废的错误记忆（勿再当真源）

| 错误记忆 | 状态 |
|----------|------|
| 「主线 = OpenWork 桌面 + OpenCode」 | **作废**（曾短暂写入，2026-08-05 业主口径覆盖） |
| 「下一刀 = 本机安装 OpenWork」 | **作废** |
| 「金路径必须在本机工作区写 hello.txt」 | **作废为唯一 G1**；现行 G1 = 浏览器可下载 HTML/文件 |
| 「Dify 只是备选、禁止改主线」 | **作废**；现行主线就是 Dify |
| 「AionUi / Eigent 与 OpenWork 并列主推」 | **作废** |
| 「主 README 以 OpenWork 为本」 | **作废** |
| 对话里未落盘的口头方案若与 CANON/HANDOFF 冲突 | **以仓内文档为准** |

## 3. 文档优先级

1. `docs/CANON.md`（本文）  
2. `docs/HANDOFF.md`  
3. `docs/PROJECT-PLAN.md` / `ops/INSTALL.md` / `ops/INFRA.md`  
4. 其它 docs、历史 Issue 评论（仅作履历，冲突时丢弃旧句）  

## 4. 允许保留的「OpenWork」字样

仅允许出现在：

- 标明 **二期 / optional / 非主线** 的段落  
- `ops/INSTALL-OPENWORK-optional.md`  
- 选型对比表中的「不选当主线」行  

**不允许**再出现：把 OpenWork 写成默认基线、阶段 A 前置、或与 Dify 并列主入口。

## 5. 仓内清理记录（本次）

- 修正 `docs/RESPONSE-LOGIC.md` 实现位置（原误写 OpenWork/OpenCode）  
- 删除主线路径下 `ops/opencode-deepseek.json.example`（旧桌面配置样例）  
- 本 CANON 落盘，供新窗开场先读  
