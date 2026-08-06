# WB-FIX-DEPLOY 部署说明

```
DATE: 2026-08-06
PHASE: PHASE-WB-FIX-DEPLOY
```

## 改了什么

### 1) Dify 工作流（现网 DB）

| 项 | 值 |
|----|-----|
| 源版本 | scene-full `898715d1-…` |
| 新版本 | **fix-deploy** `db774ef4-3eb8-42da-acb6-5982942f915a` |
| app | Aivia 课件 `fc3e14da-…` · site `lOMVPbz7rZmbJSJl` |
| 变更 | LLM 系统提示强化大纲/DOCX；PackDownload 交付清单 + DOCX/大纲门禁；`file_upload.enabled=true` |

**如何发布：** 插入 `workflows` 新行 → `update apps set workflow_id=…` → redis FLUSHDB（可选）。

### 2) bridge

| 项 | 值 |
|----|-----|
| 版本 | **0.2.2**（ALIGN 已部署，本包确认） |
| 路径 | `/home/ops/aivia-workbench/bridge` bind → container `/app` ro |
| 数据 | `/home/ops/aivia-workbench/bridge/data` → `/data` rw |
| 重启 | `docker restart aivia-bridge` |

### 3) 未改

- nginx 证书路径（LE YE2 仍有效）
- 默认 Chat site code

## 如何烟测

```bash
# bridge
docker exec aivia-bridge python -c "import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:18090/health').read())"
# ops（token 仅 secrets，不进仓）
# X-Aivia-Ops: $BRIDGE_DL_PUT_TOKEN
# GET /ops/metrics  GET /ops/policy
```

## 回滚

1. **工作流：**  
   `update apps set workflow_id='898715d1-ddbd-4405-a883-9f566634a9fb' where id='fc3e14da-2861-4009-a888-730a6b993011';`  
   （scene-full 上一稳定版）
2. **bridge：** 恢复 `server.py` 旧版本后 `docker restart aivia-bridge`（git checkout 上一 commit 的 bridge/server.py 再 scp）
3. **缓存：** `docker exec dify-redis-1 redis-cli FLUSHDB`（谨慎）

## TLS 实况（不装没事）

| 路径 | 结果 |
|------|------|
| ECS openssl s_client | CN=workbench.aivia.asia · Issuer=Let's Encrypt YE2 · 有效期至 2026-11-03 |
| ECS curl https /dl | 200 attachment |
| 部分 Windows 客户端 schannel | 可能握手失败（代理/边缘）· 已记债，不宣称全客户端零问题 |

## 密钥纪律

- `BRIDGE_DL_PUT_TOKEN` 仅 `~/.secrets/bridge.env` 与沙箱注入代码  
- **禁止** 提交真实 token；证据中的 dump 已脱敏  
