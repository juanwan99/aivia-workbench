# bridge · edu 身份与提案侧车

```
阶段: C + FIX-DEPLOY
MODE: mock
版本: 0.1.1
约束: 不直写 edu 业务库；Agent 无 apply；不公网裸奔 18090
契约: docs/EDU-BRIDGE.md
端口 PIN: 127.0.0.1:18090
```

## 运维三行

```text
启: systemctl --user start aivia-bridge
验: curl -sS http://127.0.0.1:18090/bridge/v1/health
烟: bash bridge/smoke.sh
密: ~/.secrets/bridge.env   # BRIDGE_JWT_SECRET 必填；BRIDGE_EXCHANGE_TOKEN 建议
```

安装 user unit（一次）：

```bash
cp bridge/aivia-bridge.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now aivia-bridge
loginctl enable-linger ops   # 可选：注销后仍跑
```

## 职责

1. 校验/签发 Principal（JWT）  
2. 租户隔离只读（mock）  
3. 变更提案 + 人审 API  
4. 审计日志  

## 非职责

- 替代 Dify 主 UI  
- 成绩/学籍直写 / Agent apply  
- 公网匿名 exchange  

## 密钥（F1）

| 变量 | 要求 |
|------|------|
| `BRIDGE_JWT_SECRET` | **必填**，≥24 随机字符；缺/弱 → **拒绝启动** |
| `BRIDGE_EXCHANGE_TOKEN` | **建议**；设置后 mock `/auth/exchange` 须带头 `X-Bridge-Exchange-Token` |
| `BRIDGE_HOST` | 默认 `127.0.0.1`（仅本机） |

密钥仅 env / `~/.secrets/bridge.env`，**禁止进 Git**。

## Dify 挂载（F2）

- OpenAPI：`bridge/openapi.json`  
- **现行范围（书面）：** C mock 以 API/Ce/smoke 为准；Dify 容器默认 **够不到** `127.0.0.1:18090`，工具挂载后置到 real 或单独网络方案（勿为挂载而 `0.0.0.0` 公网）。  

## 烟测

```bash
bash bridge/smoke.sh
```

全过退出 0。  
