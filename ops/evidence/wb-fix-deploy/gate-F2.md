# gate-F2
DATE: 2026-08-06
STAGE: F2
RESULT: PASS

| # | 标准 | 结果 | 证据 |
|---|------|------|------|
| R1 真文件上传 | PASS | F2/upload_resp.json id + source_material.txt |
| 再加工出 /dl | PASS | F2/upload_rework.html · answer 含 DOWNLOAD_READY 清单 |
| 配置可指 | PASS | workflow features.file_upload.enabled=true（fix-deploy 版本） |

## 复现步骤
1. `POST /v1/files/upload`（app API key）上传 .txt
2. `POST /v1/chat-messages` 带 `files[].upload_file_id`
3. 回答含 https `/dl` 交付清单；下载文件本机可开

## 空成功: 0
## 进入 F3: YES
