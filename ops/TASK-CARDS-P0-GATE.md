# 标准任务卡 · PHASE-P0-GATE

```
DATE: 2026-08-06
包: ops/PHASE-P0-GATE-PACK.md
硬门禁: RUNBOOK+证据+PIN/CANON+Issue+push · 缺一不许报完毕
```

---

## 卡 0 · 波 0 稳定（先做）

```
════════════════════════════════════
标准任务卡 · P0-STAB
════════════════════════════════════
执行窗：现网运维 + 轻文档
上下文：E1 仓内 PASS · 外网曾 RST/打开慢 · CLAIM-B 未勾
角色：HTTPS 稳 + 续期 + 真源一致
RISK: 黄（nginx/WAF；勿裸停；AK 不进 Git）
【硬门禁·回写】P0-GATE-RUNBOOK 波0 · evidence/p0-stab 可选 · PIN/README/CANON · Issue
【真源】PHASE-P0-GATE-PACK §2 → P0-GATE-RUNBOOK
【做】公网 TLS 连测 · 4G 有壳 · 续期策略 · 修 SNI/WAF · 去自签旧句
【不做】假 CLAIM-B · 重刷 B 电池充数 · 公网裸 bridge
【出口】波0 PASS 或 BLOCKED+原因
BASE：https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl
════════════════════════════════════
```

---

## 卡 1 · 波 1 金路径体感

```
════════════════════════════════════
标准任务卡 · P0-GOLD
════════════════════════════════════
执行窗：执行窗/运维跑路径 · 可选改提示词
上下文：波0 PASS（或业主书面豁免残留）
角色：G1/G1+/G2/G3/G4 体感 · 空成功0 · 对标一线出件
RISK: 低～中（模型波动；禁关限流）
【硬门禁·回写】RUNBOOK 波1 · ops/evidence/p0-gold/ · P0-GOLD-REPORT · Issue
【真源】PHASE-P0-GATE-PACK §3
【做】五刀金路径 · 下载可点 · 大纲不假绿 · 失败人话
【不做】装饰假按钮 · Harness · 冒充 CLAIM-B
【出口】波1 PASS · 空成功0
════════════════════════════════════
```

---

## 卡 2a · CLAIM-B 验收

```
════════════════════════════════════
标准任务卡 · CLAIM-B
════════════════════════════════════
执行窗：产品 + 真用户眼（可业主自己）
上下文：波0+波1 PASS
角色：教师正式可用门禁
RISK: 低（纪律：≠全校上线）
【硬门禁·回写】CLAIM-B-RUNBOOK · PIN CLAIM-B=YES · SCRIPT · Issue
【真源】PHASE-P0-GATE-PACK §4 · CLAIM-B-RUNBOOK
【做】B1–B8 桌面+4G · G1/G1+/G3 · 五句话术
【不做】自动正式全校 · 要求 full real 才过 · 假截图
【出口】CLAIM-B PASS · 正式上线默认仍否
════════════════════════════════════
```

---

## 卡 2b · FULL-REAL（可并行，不顶替 2a）

```
════════════════════════════════════
标准任务卡 · FULL-REAL
════════════════════════════════════
执行窗：bridge 研发 + edu 对接 + Dify
上下文：hybrid 绿 · 需 edu 只读 API
角色：MODE=real · live 只读 · 工具命中
RISK: 黄（身份/网络；禁写库；禁公网裸 exchange）
【硬门禁·回写】FULL-REAL-RUNBOOK · EDU-BRIDGE v0.3 · PIN real · Issue
【真源】PHASE-P0-GATE-PACK §5 · PHASE-C-REAL-PACK 继承
【做】R0–R5 · Ce-R · smoke · 脱敏证据
【不做】fixture 冒充 full · 假 CLAIM-B · Agent apply
【出口】CLAIM-C-REAL full
════════════════════════════════════
```

---

## 执行口令

1. **必须先卡 0，再卡 1**  
2. 卡 2a / 2b 业主点名先后；**禁止跳过 0/1 勾 CLAIM-B**  
3. 每卡结束：回写 → 再报「完毕」  
