# QUAD-FIX-DEPLOY 部署说明与回滚

```
DATE: 2026-08-06
PHASE: PHASE-QUAD-FIX-DEPLOY
CLAIM: CLAIM-QUAD-FIX-DEPLOY
```

## 改了什么

### F1 / X1 · nginx 专家入口

| 面 | 变更 |
|----|------|
| **dmit 边缘** | `asyncova-workbench-locations.inc`：`/experts` 与 `/experts/` **均 200 直接出页**，禁止 `return 302` 触发 `:8443` |
| **ECS 源站** | `workbench.aivia.asia.conf` 同步：`alias` 精确匹配文件 + 目录，无斜杠跳转依赖 |

根因：SSL 终止在 `127.0.0.1:8443`，相对 `return 302 /experts/` 被 nginx 拼成 `https://host:8443/...`。

### F2 / X2 · 隧道 systemd

| 项 | 值 |
|----|-----|
| 单元 | `~/.config/systemd/user/aivia-edge-tunnel.service`（user 级） |
| 修复 | **去掉 `User=ops`**（user unit 写 User= → status=216/GROUP） |
| 行为 | `ssh -N -R 127.0.0.1:13080:127.0.0.1:13080 dmit` · Restart=always |
| probe | dmit: `curl 127.0.0.1:13080/chat/...` → 200 |

### P1 / X3

- `ops/evidence/quad-fix-deploy/experts/catalog.yaml`
- 本 NOTES（含回滚）

## 如何验收

```bash
# 专家（禁止出现 Location: ...:8443）
curl -sI https://asyncova.com/experts | head
curl -sI https://asyncova.com/experts/ | head
# Chat + dl
curl -sI https://asyncova.com/chat/lOMVPbz7rZmbJSJl | head
# 隧道
ssh ecs 'systemctl --user status aivia-edge-tunnel.service --no-pager | head'
ssh dmit 'curl -s -o /dev/null -w %{http_code} -H Host:workbench.aivia.asia http://127.0.0.1:13080/chat/lOMVPbz7rZmbJSJl'
```

## 回滚

### 边缘 nginx

```bash
# dmit
sudo cp /etc/nginx/conf.d/asyncova.com.conf.bak-quad-* /etc/nginx/conf.d/asyncova.com.conf  # 若仅改 locations
# 恢复 locations 到「带 302」旧版（不推荐）或去掉 include：
# 编辑 asyncova.com.conf 删除 include asyncova-workbench-locations.inc
sudo nginx -t && sudo systemctl reload nginx
```

当前 locations 文件可从 git：`ops/evidence/quad-fix-deploy/edge/asyncova-workbench-locations.inc` 重装。

### 源站 nginx

```bash
# ecs — 备份在 conf.d
docker run --rm -v /etc/nginx/conf.d:/cfg alpine \
  ls /cfg/workbench.aivia.asia.conf.bak*
# 恢复某一 bak 后
sudo systemctl reload nginx
```

### 隧道

```bash
ssh ecs 'systemctl --user stop aivia-edge-tunnel.service'
# 或 nohup 手工：
# ssh -N -R 127.0.0.1:13080:127.0.0.1:13080 dmit
```

## 未改

- Dify workflow / app site code  
- FULL-REAL（仍 NO）  
- 正式上线范围（仍「是（受限）」· 不扩大全校）  
- 密钥不进仓  
