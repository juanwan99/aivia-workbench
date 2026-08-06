# gate-Q3 · full real

| 项 | 结果 | 说明 |
|----|------|------|
| bridge MODE | hybrid | health 0.2.2 |
| MODE=real 可启 | NO | server.py 无 live edu adapter 直接 FATAL |
| edu 只读 live | NO | 未接线 |
| FULL-REAL | **NO** | DEGRADED · 禁假绿 |
| fixture 冒充 live | 禁止 | 保持 hybrid 诚实 |

**RESULT: PASS（诚实 DEGRADED）** · `FULL-REAL=NO`
