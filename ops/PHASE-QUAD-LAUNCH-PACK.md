# 任务包 · PHASE-QUAD-LAUNCH（四线大包 · 无人值守）

```
STATUS: DONE · CLAIM-QUAD-LAUNCH=YES · FULL-REAL=NO · 正式上线=是（受限）
DATE: 2026-08-06
CODE: PHASE-QUAD-LAUNCH
形态: Dify Web + DeepSeek + bridge · 公网边缘 asyncova.com
模式: Q0→Q5 自审过门 · 中途不请示
```

## 0. 完成定义（整包唯一 CLAIM）

```text
CLAIM-QUAD-LAUNCH 整包 PASS 当且仅当：
  [ ] Q0 survey 文件存在
  [ ] Q1 TLS：公网全链 · Chrome/Edge 可证 · 4G 同公网路径 · 续期书面 · /dl 可下载
  [ ] Q2 /experts ≥4 卡 · ≥2 卡真出件（证据进仓）
  [ ] Q3 FULL-REAL=YES|NO 诚实；无 API 则 DEGRADED 禁假绿
  [ ] Q4 CHECKLIST+AUTH · 正式上线字段写清限制
  [ ] ops/evidence/quad-launch/ gate* + REPORT
  [ ] PIN/CANON 回写 · Issue · push main
禁止：抄 WB 像素 · 假 full real · 跳 TLS 上线 · 花架专家 · 写库 · 密钥进仓
```

## 1. 四线定义

### Q1 TLS

| 项 | 过线 |
|----|------|
| 全链 | 公网 openssl/浏览器无自签惊吓（边缘域名 LE 或有效链） |
| Chrome/Edge | 桌面打开入口 Chat 200 · 无证书警告（证据截图或协议记录） |
| 4G | 与公网同入口；机房外实测或声明同路径 |
| 续期 | 源站 acme.sh DNS-01；边缘 asyncova webroot 续期备注 |
| 可下载 | `/dl` GET → Content-Disposition: attachment |

### Q2 专家壳

| 项 | 过线 |
|----|------|
| 路由 | `GET /experts` 200 · ≥4 可见卡 |
| 真出件 | ≥2 卡路径跑通 DOWNLOAD_READY + 真文件 |

### Q3 full real

| 条件 | 动作 |
|------|------|
| edu live API 就绪 | MODE=real · 勾 FULL-REAL=YES |
| 未就绪 | DEGRADED · FULL-REAL=NO · 禁报 full |

### Q4 上线

| 项 | 过线 |
|----|------|
| CHECKLIST | `ops/QUAD-LAUNCH-CHECKLIST.md` 勾满 |
| AUTH | 授权范围书面（本包=受限公测/教师默认链） |
| 正式上线 | 字段=是 **且** 限制段非空 |

## 2. 关联

- 调查：`ops/QUAD-LAUNCH-SURVEY.md`
- 勾选：`ops/QUAD-LAUNCH-RUNBOOK.md`
- 报告：`ops/QUAD-LAUNCH-REPORT.md`
- 证据：`ops/evidence/quad-launch/`
