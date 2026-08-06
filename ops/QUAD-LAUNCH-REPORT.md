# QUAD-LAUNCH 报告

```
DATE: 2026-08-06
PHASE-QUAD-LAUNCH: PASS
CLAIM-QUAD-LAUNCH: YES
FULL-REAL: NO
正式上线: 是（受限）
空成功: 0
公网入口: https://asyncova.com
```

## 1. 结论（一句话）

四线收口：**公网 TLS（海外边缘）可开可下**、**专家目录 5 卡且 2 卡真出件**、**full real 诚实 NO**、**正式上线=是（受限）**；可报 **CLAIM-QUAD-LAUNCH=YES**。

## 2. 四线结果

| 线 | 结果 | 要点 |
|----|------|------|
| Q1 TLS | PASS | 源站 LE 全链保留；公网主入口 `asyncova.com` LE YE2；/dl attachment；Windows schannel 200 |
| Q2 专家壳 | PASS | `/experts` 5 卡；HTML+DOCX 真文件 |
| Q3 full real | DEGRADED | hybrid · **FULL-REAL=NO** · 禁假绿 |
| Q4 上线 | PASS | CHECKLIST+AUTH · 正式上线=是（受限） |

## 3. 入口

| 用途 | URL |
|------|-----|
| 专家目录 | https://asyncova.com/experts |
| 默认 Chat | https://asyncova.com/chat/lOMVPbz7rZmbJSJl |
| 下载 | https://asyncova.com/dl/... |
| 源站域名 | workbench.aivia.asia（机房内 OK；大陆公网 ICP 拦） |

## 4. 架构处置（本窗）

1. **根因：** 阿里云大陆 EIP 对未备案 `*.aivia.asia` 做 Beaver/SNI 拦截。  
2. **公网边缘：** dmit `asyncova.com` nginx 路径反代 → SSH 反向隧道 → ECS Dify `:13080`。  
3. **专家页：** 边缘静态 `/var/www/aivia-experts` + 源站 `/experts`（/var/www）。  
4. **bridge：** `public_dl_base=https://asyncova.com/dl` · 仍 hybrid 0.2.2。  
5. **sub_filter：** 边缘将响应中的 workbench 绝对链改写为 asyncova（辅助）。

## 5. 证据

目录：`ops/evidence/quad-launch/`

| 文件 | 用途 |
|------|------|
| gate-Q0…Q5.md | 自审门禁 |
| q1-public-probe.txt | 公网 Chat/experts/dl |
| tls-origin.txt / tls-edge.txt | 证书 |
| quad-launch-q2/* | 两卡真出件 |
| experts/index.html | 专家壳源 |
| edge/* | 隧道与 nginx 片段 |

## 6. 限制（正式上线=是 的边界）

1. **≠ 全校推广**；仅受限公测 / 教师默认链。  
2. **FULL-REAL=NO**；edu live 未接。  
3. **workbench.aivia.asia 不作大陆公网主入口**（ICP）。  
4. **≠ WorkBuddy 1:1**；专家壳 clean-room。  
5. **边缘依赖：** ECS→dmit SSH 反向隧道需保活（nohup/user service）。  
6. **asyncova.com** 与 Aivia 品牌并存为技术绕行；后续可迁已备案专用域名。  
7. 密钥 / ops token **不进仓**。

## 7. 续期

| 面 | 策略 |
|----|------|
| 源站 workbench | acme.sh DNS-01 手工 TXT；建议 dns_ali |
| 边缘 asyncova | certbot webroot · 续期至 ~2026-10-28 |

## 8. CLAIM 出口

```text
CLAIM-QUAD-LAUNCH: YES
FULL-REAL: NO
正式上线: 是（受限）
= Q1 公网 TLS 可开可下 + Q2 专家真出件 + Q3 诚实 DEGRADED + Q4 CHECKLIST/AUTH
≠ 全校推广 · ≠ full real · ≠ 备案完成
```

## 9. 禁止复读

- 假 full real / 假全校上线  
- 跳 TLS 上线  
- 花架专家（无真出件）  
- 密钥进仓 · Agent 写库 · 抄 WB 像素  
