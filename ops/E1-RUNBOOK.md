# E1 正式证书 · 勾选清单

日期：2026-08-06    执行人：phase-e1-run（ECS）  
路径：DNS-01 手工 / acme.sh dns_ali / 云证书（圈一）→ **未完成 · BLOCKED**

## 现网事实

| 项 | 结果 |
|----|------|
| 证书 | **仍自签**（CN=workbench.aivia.asia · issuer 自签） |
| 浏览器校验 | `CERTIFICATE_VERIFY_FAILED: self-signed certificate` |
| HTTP-01 | **不做死磕**（历史：外网 LE 403/空 body） |
| DNS-01 依赖 | 阿里云 DNS（NS=`dns1/2.hichina.com`） |
| 本机 AK | **无** 阿里云 DNS API 密钥（禁止长驻 Git） |
| certbot | 本机 CLI 依赖破损（josepy/OpenSSL AttributeError） |
| 权限 | `/etc/letsencrypt` · nginx conf **root 属主**；执行窗无 sudo |
| nginx 路径 | 已指向 `live/workbench.aivia.asia/fullchain.pem`（待替换真证书） |

## 勾选

- [ ] TXT 或证书申请完成  
- [ ] nginx 指向 fullchain + privkey（路径已预留，内容仍自签）  
- [ ] `nginx -t` + `systemctl reload nginx`  
- [ ] 浏览器无警告  
- [ ] 默认 Chat 可聊  
- [ ] 课件下载冒烟  
- [ ] 外网/4G 复验  
- [x] Issue「E1 **BLOCKED**」  
- [x] DEBT-LEDGER + PIN + INFRA 更新  

**结果：** **BLOCKED**（非 FAIL 产品；门禁诚实）  
**备注：** 解锁见下；**禁止** 借机勾 CLAIM-B  

## 解锁步骤（业主）

1. 提供 DNS-01 能力之一：  
   - 阿里云 DNS AK（仅运维私密，**不进 Git**）+ `acme.sh --dns dns_ali` 或 certbot dns 插件  
   - 或控制台手工加 `_acme-challenge.workbench` TXT（交互式 certbot/acme）  
   - 或云厂商托管证书下载 fullchain+key  
2. 修复/使用可用 ACME 客户端（修复 certbot 依赖或改 acme.sh）  
3. root：安装到 `/etc/letsencrypt/live/workbench.aivia.asia/`  
4. `nginx -t && systemctl reload nginx`  
5. 本机 `openssl s_client` / 浏览器 **无警告**  
6. 默认 Chat 可聊 + 下载 + **外网/4G 复验**  
7. Issue 改「E1 PASS」→ 方可谈 CLAIM-B  

```text
E1: BLOCKED
原因: 无 DNS API/手工窗 + 无 root 写证书 + certbot 破损；仍自签
CLAIM-B: NO
```
