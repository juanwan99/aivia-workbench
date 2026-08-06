# gate-X1 F1 nginx

| 项 | 结果 | 证据 |
|----|------|------|
| /experts 200 | PASS | f1-experts-public.txt Path=exact |
| /experts/ 200 | PASS | Path=slash |
| 无 Location:8443 | PASS | Select-String 无匹配 |
| 源站双路径 | PASS | workbench conf alias |

**RESULT: PASS**
