# bridge · edu 身份与提案侧车

```
阶段: C
约束: 不直写 edu 业务库；Agent 无 apply
契约: docs/EDU-BRIDGE.md
执行: ops/PHASE-C-PACK.md
```

## 职责

1. 校验/签发 Principal（JWT）  
2. 租户隔离的只读代理  
3. 变更提案存储与人审 API  
4. 审计日志  

## 非职责

- 替代 Dify 主 UI  
- 成绩/学籍直写  
- 像素级改 Dify 核  

## 开发顺序

1. C0 契约确认  
2. 最小服务：`/me` + mock classes + proposals  
3. Docker/compose 侧挂现网  
4. Dify 自定义工具对接  
5. Ce 金路径  

## 本地（规划）

```bash
# 待 C1 起补充真实启动命令与端口 PIN
# 例: docker compose -f bridge/docker-compose.yml up -d
```

密钥仅 env：`BRIDGE_JWT_SECRET`、`EDU_BASE_URL` 等。
