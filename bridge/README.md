# bridge · edu 身份与提案侧车

```
阶段: C
MODE: mock
约束: 不直写 edu 业务库；Agent 无 apply
契约: docs/EDU-BRIDGE.md
执行: ops/PHASE-C-PACK.md
端口 PIN: 127.0.0.1:18090
```

## 职责

1. 校验/签发 Principal（JWT）  
2. 租户隔离的只读代理（mock 数据）  
3. 变更提案存储与人审 API  
4. 审计日志  

## 非职责

- 替代 Dify 主 UI  
- 成绩/学籍直写  
- 像素级改 Dify 核  

## 启动

```bash
export BRIDGE_JWT_SECRET='…'   # 仅服务器 env，勿进 Git
export BRIDGE_MODE=mock
export BRIDGE_HOST=127.0.0.1
export BRIDGE_PORT=18090
python3 bridge/server.py
# 或: bash bridge/run.sh
```

健康检查：`curl -s http://127.0.0.1:18090/bridge/v1/health`

## Mock 换票

```bash
curl -s -X POST http://127.0.0.1:18090/bridge/v1/auth/exchange \
  -H 'Content-Type: application/json' \
  -d '{"sub":"t-demo","school_id":"school-demo","role":"teacher","name":"演示教师"}'
```

密钥仅 env：`BRIDGE_JWT_SECRET`。  
