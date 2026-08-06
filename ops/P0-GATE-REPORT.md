# P0-GATE 短报告

```
DATE: 2026-08-06
入口: https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl
P0-GATE: PASS
CLAIM-B: YES
正式上线: 否
full real: 跳过（hybrid）
空成功: 0
```

## 1. 结论（一句话）

公网 TLS（LE）稳定、默认 Chat 金路径 **G1/G1+/G2/G3/G4 全过且空成功 0**，可报 **CLAIM-B=教师正式可用（公开默认链）**；**不**等于全校正式上线，**不**等于 edu full real。

## 2. 段 A 稳定

| 项 | 结果 |
|----|------|
| A1 TLS×3 | PASS · YE2 · TLSv1.3 |
| A2 桌面壳 | PASS · Chat 200 |
| A3 公网路径 | PASS（与 4G 同公网入口；建议人眼 4G 点验） |
| A4 续期 | 现行：acme.sh **手工 DNS-01**；推荐升级：阿里云 `dns_ali` 自动 |
| A5 真源 | 本报告窗口同步 CANON/PIN/README |
| A6 bridge | hybrid 0.2.0 · health 200 · 匿名 exchange 401 |

**限流备注（既有修复）：** SPA 静态资源曾被 `30r/m` 打死；现 `60r/s` / burst 120，避免「能握手但页面转圈」。

## 3. 段 B 金路径

| ID | 结果 | 证据 |
|----|------|------|
| G1 HTML 下载 | PASS | `g1-artifact.html` |
| G1+ 改稿 | PASS | `g1plus-artifact.html` |
| G2 教案 md | PASS | `g2-artifact.md` |
| G3 大纲无假文件 | PASS | `g3-answer.head.txt` |
| G4 失败诚实 | PASS | `g4-answer.head.txt`（拒写库） |

**空成功：0** · meta：`ops/evidence/p0-gate/p0-meta.json`

## 4. 段 C CLAIM-B

按 PACK 定义完成：默认公开链接可打开、可要课件下载、可改稿、大纲不假绿、话术定稿。  
**PIN：`CLAIM-B=YES`** · **正式上线：否**（未授权全校推广）。

老师话术：`ops/CLAIM-B-SCRIPT.md`

## 5. 段 D

**跳过 full real** — 保持 **CLAIM-C-REAL(hybrid)**。edu 业务只读 API 未挂前禁止报 full real。

## 6. 风险与下一刀

| 风险 | 说明 |
|------|------|
| 边缘 WAF | 部分外网曾报 SNI RST；源站本机 SNI 正常，需业主 4G 确认 |
| 续期 | 手工 TXT 需记得改 dns_ali |
| 模型波动 | 空成功门禁；回归可再跑 G1 |

**下一刀（择一）：**  
1. 业主 4G 人眼确认 + 需要时开 CLAIM-B 运营通知（仍非全校）  
2. edu live 只读 → full real  
3. 证书 dns_ali 自动续期  

## 7. 禁止复读

- 假全校上线  
- 跳过 A/B 勾 CLAIM-B  
- Agent 写库 · Harness 主线 · 密钥进仓  
