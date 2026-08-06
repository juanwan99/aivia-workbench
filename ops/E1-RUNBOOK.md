# E1 正式证书 · 勾选清单

日期：2026-08-06    执行人：phase-e1-run（ECS）+ 业主阿里云 DNS  
路径：acme.sh **DNS-01 手工**（路径 A）  

## 现网结果

| 项 | 结果 |
|----|------|
| CA | **Let's Encrypt YE2** |
| 域名 | `workbench.aivia.asia` |
| 有效期 | ~2026-11-03 |
| 客户端 | `~/.acme.sh`（LE） |
| 装载路径 | `/etc/letsencrypt/live/workbench.aivia.asia/{fullchain,privkey}.pem` |
| nginx | reload OK |

## 勾选

- [x] TXT 完成（`_acme-challenge.workbench`）  
- [x] nginx 指向 fullchain + privkey（路径未改，内容已换 LE）  
- [x] reload nginx（`systemctl reload nginx`）  
- [x] 系统 TLS 校验无警告（VERIFY_OK TLSv1.3）  
- [x] 默认 Chat 可开（HTTPS 200）  
- [x] 课件下载冒烟（G1 DOWNLOAD_READY）  
- [ ] 外网/4G 复验（**请业主手机再开一次**）  
- [x] Issue「E1 PASS」  
- [x] DEBT-LEDGER + PIN + INFRA 更新  

**结果：** **PASS**（机房侧验收满；4G 请业主补一眼）  
**备注：** 续期建议改 DNS API（路径 B）；手工 TXT 每次续期需再贴。**CLAIM-B 未自动勾**（需另门禁）。  

```text
E1: PASS
CA: Let's Encrypt YE2
CLAIM-B: 可谈（未在本窗自动勾）
```
