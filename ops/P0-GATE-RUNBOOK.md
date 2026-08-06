# P0-GATE 勾选（单包单卡）

日期：2026-08-06    执行人：phase-p0-gate（ECS）  
入口：`https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl`  
正文：`ops/PHASE-P0-GATE-PACK.md`  
证据：`ops/evidence/p0-gate/`

## 硬门禁

- [x] 本文件填满  
- [x] `ops/evidence/p0-gate/` 证据  
- [x] `ops/P0-GATE-REPORT.md`  
- [x] `ops/CLAIM-B-SCRIPT.md`  
- [x] PIN + CANON/HANDOFF/README  
- [x] Issue #1 + push main  
→ 缺一不得报 P0-GATE PASS

---

## 段 A 稳定

- [x] A1 公网 TLS ×3：**PASS**（TLSv1.3 · LE YE2 · 3/3）  
- [x] A2 桌面壳：**PASS**（Chat HTTPS 200 · ~468KB）  
- [x] A3 4G 壳：**PASS**（公网域名 TLS+Chat 同源路径已验；建议人眼 4G 再点一次）  
- [x] A4 续期：**手工 DNS-01（acme.sh）**；升级路径 dns_ali 书面见报告  
- [x] A5 真源去滞后：**PASS**（本窗回写）  
- [x] A6 bridge health 200 · MODE=hybrid · 无 token exchange **401**  
- **A 结果：** **PASS**

## 段 B 金路径（空成功必须 0）

| ID | 结果 | 产物 |
|----|------|------|
| G1 | **PASS** | `g1-artifact.html` · DOWNLOAD_READY |
| G1+ | **PASS** | `g1plus-artifact.html` · 同会话改稿 |
| G2 | **PASS** | `g2-artifact.md` |
| G3 | **PASS** | 大纲 only · 无 DOWNLOAD_READY |
| G4 | **PASS** | 诚实拒绝写库/大上传（见 g4-answer.head.txt） |

空成功次数：**0**  
计分 meta：`ops/evidence/p0-gate/p0-meta.json`

## 段 C CLAIM-B

- [x] C1 桌面 + G1  
- [x] C2 公网可达 + 能聊（4G 人眼建议补一眼）  
- [x] C3 G1+  
- [x] C4 G3  
- [x] C5 SCRIPT 定稿  
- [x] C6 PIN **CLAIM-B=YES** · **正式上线=否**  
- **CLAIM-B：** **YES**

## 段 D full real

- [x] **跳过**（hybrid 保持）  
- **说明：** edu-core BFF 仅 `/health`，业务只读 API 未就绪 → **不报 full real**

## 整包

```text
P0-GATE: PASS
CLAIM-B: YES
full real: 跳过（hybrid）
正式上线: 否
空成功: 0
```
