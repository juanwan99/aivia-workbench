# QUAD-LAUNCH 水位调查（Q0）

```
DATE: 2026-08-06
CODE: PHASE-QUAD-LAUNCH
STATUS: SURVEY
执行窗: 本机 Grok + SSH ecs(ProxyJump) + dmit 边缘
```

## 1. 已收底盘（勿重做）

| 项 | 状态 |
|----|------|
| CLAIM-B / DOC-SOLID / DL-FIX / SCENE-FULL | YES |
| WB-SURVEY / WB-ALIGN / WB-FIX-DEPLOY | YES |
| bridge | 0.2.2 hybrid · `/dl` · ops |
| workflow | fix-deploy |
| Chat site | `lOMVPbz7rZmbJSJl` |
| 源站证书 | LE YE2 · CN=workbench.aivia.asia · 至 2026-11-03 |

## 2. 关键阻塞（本窗实测）

### 2.1 TLS / 公网可达

| 路径 | 结果 |
|------|------|
| ECS 本机 SNI=`workbench.aivia.asia` | **PASS** · 全链 VERIFY_OK（ISRG X2→YE→YE2） |
| ECS 本机 `/chat` · `/dl` GET | **PASS** · 200 attachment |
| 外网 SNI=`workbench.aivia.asia` → 47.121.197.52:443 | **FAIL** · ClientHello 后 RST |
| 外网 HTTP/80 Host=workbench | **403 Beaver** · 标题 **Non-compliance ICP Filing** |
| 对照 SNI=`mcu.asia` / `edu.weiyuji.cn` | **PASS**（已备案域名） |
| 对照 SNI=`asyncova.com`（dmit 154.17.0.72） | **PASS**（海外节点 · 无 ICP 拦截） |

**根因：** 大陆 EIP 对未备案域名 `*.aivia.asia` 做 SNI/HTTP 拦截；**不是**证书本身坏了。  
**本包策略：** 保留源站 LE；**公网入口切到海外已证域名** `https://asyncova.com`（路径级反代 + 隧道），Chrome/Edge/4G 可走通。

### 2.2 专家壳

| 项 | 现状 |
|----|------|
| `/experts` | **无** |
| WB 对标 E-01 | 后置项 · 本包落地 clean-room 专家目录（非抄像素） |

### 2.3 full real

| 项 | 现状 |
|----|------|
| bridge MODE | hybrid |
| MODE=real 启动 | **拒绝**（live edu adapter 未实现） |
| edu 只读 live API | **未挂到 bridge** |

→ Q3 默认 **DEGRADED / FULL-REAL=NO**，禁假绿。

### 2.4 正式上线

| 项 | 现状 |
|----|------|
| PIN 正式上线 | 否 |
| CLAIM-B | YES（教师默认链可用 · 非正式全校推广） |

→ Q4 写清限制后可勾 **正式上线=是（受限）**。

## 3. 执行边界

**做：** Q1 公网 TLS 全链可开可下 · Q2 `/experts`≥4 卡且≥2 真出件 · Q3 诚实 full real · Q4 CHECKLIST+AUTH · 证据/报告/PIN/Issue  

**不做：** 抄 WB 像素 · 假 full real · 跳 TLS 上线 · 花架专家 · Agent 写库 · 密钥进仓 · 改阿里云 DNS（本窗 RAM 无权限）

## 4. 目标入口（本包）

| 用途 | URL |
|------|-----|
| **公网主入口（绕 ICP）** | `https://asyncova.com/chat/lOMVPbz7rZmbJSJl` |
| 专家目录 | `https://asyncova.com/experts` |
| 下载 | `https://asyncova.com/dl/{id}/file.{ext}` |
| 源站（机房内/对照） | `https://workbench.aivia.asia/...`（外网仍可能被 ICP 拦） |

## 5. 过门序列

`Q0 survey → Q1 TLS → Q2 experts → Q3 full-real → Q4 launch → Q5 claim`
