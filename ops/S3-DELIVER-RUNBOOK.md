# S3-DELIVER Runbook

1. 打开 Chat / experts，按 `TASK-CARD-S3-DELIVER.md` §2 测句走查。  
2. 截图保存到 `ops/evidence/general-wb/s3/ui/`（文件名见卡）。  
3. FAIL 项 → R1–R4 修复部署 → 复截。  
4. 填写 gate-U*、s3-meta.json、S3-UX-REPORT.md。  
5. 更新 PIN、TASK-CARD-NOW。  
6. `git add ops/evidence/general-wb/s3 ops/S3-UX-REPORT.md upstream/PIN.md ops/TASK-CARD-NOW.md && git commit && git push`。  
7. `gh api repos/juanwan99/aivia-workbench/contents/ops/evidence/general-wb/s3/ui` 确认远端有图。  
8. 仅此时 CLAIM-S3-UX=YES。
