# 阶段 B 硬化包（历史 · 应用侧已完成）

```
STATUS: 应用硬化 H1/H3/H7 已收（2026-08-05）· 剩余债务转 PHASE-DEBT-CLEAR
```

执行结果见 `ops/B-HARDEN-RUNBOOK.md` · `ops/PHASE-B-CLOSEOUT.md` · `upstream/PIN.md`。

**新窗不要从本包重做 Harden。**  
**当前唯一执行包：** [`ops/PHASE-DEBT-CLEAR-PACK.md`](./PHASE-DEBT-CLEAR-PACK.md)

---

（以下为历史设计正文，供追溯）

## 原目标

把有条件 M3 推到可对内演示的应用硬化；正式公网仍看 H2（现 E1）。

## 原完成定义（已满足应用侧）

- [x] H1 真下载（data-URL 控件）  
- [x] H3 并发+nginx  
- [x] H7 五次回归空成功 0  
- [ ] H2 正式证书 → **改由 DEBT-CLEAR E1**  

## 关联

| 文件 | 用途 |
|------|------|
| `PHASE-DEBT-CLEAR-PACK.md` | **当前** |
| `B-HARDEN-RUNBOOK.md` | 历史勾选结果 |
| `PHASE-B-CLOSEOUT.md` | 收口 |
