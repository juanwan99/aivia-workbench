# S1-GENERAL-WB 报告

```
DATE: 2026-08-06
PHASE: S1-GENERAL-WB
CLAIM-S1-GENERAL-WB: YES
W0+G1–G3: 全绿
空成功: 0
FULL-REAL: NO（未扩大）
正式上线: 是（受限）· 未扩大
```

## 1. 结论

默认 Chat 入口从「课件/教案」教育主叙事改为 **Aivia 通用 Agent**。  
W0 文案与系统提示过线；G1 Word、G2 Excel 公网 `/dl` 可下可开；G3 短答无假 DOWNLOAD。  
可报 **CLAIM-S1-GENERAL-WB=YES**。G4–G7 不在本卡。

## 2. 变更

| 项 | 前 | 后 |
|----|----|-----|
| App 名 | Aivia 课件 | **Aivia 通用 Agent** |
| workflow | fix-deploy | **general-wb-s1** `a853ac87-…` |
| 系统提示 | 课件/教案/报表多场景 | 办公/表/公号/代码/分析/改稿 |
| 开场白 | HTML 课件、Word 教案… | 通用 Agent 六域 |
| 推荐问题 | 4 条教研向 | **8 条通用域** |
| PackDownload | 沿用 | **未改 token**（仅提示词+features） |

## 3. 门禁

| 门 | RESULT | 要点 |
|----|--------|------|
| W0 | **PASS** | 通用系统提示 · 8 推荐 · 无「仅教研」 · App 更名 |
| G1 | **PASS** | docx 2488 B · ooxml · asyncova `/dl` 200 |
| G2 | **PASS** | xlsx 1906 B · ooxml · asyncova `/dl` 200 |
| G3 | **PASS** | 正文 `2。` · 无 /dl · 无 DOWNLOAD_READY |

## 4. 证据

根目录：`ops/evidence/general-wb/s1/`

- gates · `results.json` · `parameters.json`  
- 产物：`g1-docx.docx` / `g2-xlsx.xlsx` / `public-g*.{docx,xlsx}`  
- 发布/电池脚本（无密钥）

## 5. 限制（诚实）

- **≠ CLAIM-GENERAL-WB**（需 S2 G4–G7）  
- FULL-REAL 仍 NO · 正式上线未扩大  
- 教育场景仍可做，但不再是默认主叙事  
- 未做备案域名 / dns_ali  

## 6. CLAIM

```text
CLAIM-S1-GENERAL-WB: YES
= W0 通用入口 + G1 Word/dl + G2 Excel/dl + G3 短答真绿 + 证据
≠ G4–G7 · ≠ full real · ≠ 全校上线
```

## 7. 下一刀

**S2-GENERAL-WB（G4–G7）** → 再冲击 CLAIM-GENERAL-WB
