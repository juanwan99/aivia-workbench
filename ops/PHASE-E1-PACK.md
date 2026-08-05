# 阶段 E1 · 正式证书 + 公网（唯一 P0 剩余债）

```
STATUS: BINDING · 当前唯一必做运维包
DATE: 2026-08-05
门: CLAIM-A / CLAIM-B / 教师正式话术
```

> 应用侧 DEBT-CLEAR 已收。本包**只做证书与可达**，不重做 A/B/C。

## 为何 HTTP-01 失败（已证）

- 本机 ACME webroot **有 body**
- **外网** Let's Encrypt 校验 **403 / 空 body**（WAF/路径阻断）
- → **必须 DNS-01 或云厂商证书**，勿再死磕 HTTP-01

## 路径甲 · certbot DNS-01 手工（推荐，无 AK）

在**现网服务器**执行（示意）：

```bash
# 1) 申请（会提示添加 TXT）
sudo certbot certonly --manual --preferred-challenges dns \
  -d workbench.aivia.asia \
  --agree-tos -m admin@aivia.asia \
  --preferred-chain "ISRG Root X1"

# 2) 按提示到【阿里云 DNS】添加：
#    主机记录: _acme-challenge.workbench
#    类型: TXT
#    值: certbot 给出的字符串
# 等待解析生效后再回车继续

# 3) 挂到 nginx（路径按实际 live 目录）
# ssl_certificate     /etc/letsencrypt/live/workbench.aivia.asia/fullchain.pem;
# ssl_certificate_key /etc/letsencrypt/live/workbench.aivia.asia/privkey.pem;

# 4) 只 reload，禁止裸 stop
sudo nginx -t && sudo systemctl reload nginx
```

## 路径乙 · acme.sh + 阿里云 DNS API

- 业主提供**仅 DNS 编辑** RAM AK（**勿进 Git / 勿贴 Issue**）
- 服务器临时环境变量 → `acme.sh --issue --dns dns_ali -d workbench.aivia.asia`
- 装载 nginx 后 **立即作废/删除** 临时 AK 环境变量

## 路径丙 · 云厂商 / 现成证书

- 在阿里云 SSL 控制台申请免费证书 → 下载 → 放到服务器 → nginx 引用 → reload

## 验收（E1 PASS 硬条件）

```text
[ ] 浏览器打开 https://workbench.aivia.asia 无证书警告
[ ] 打开 https://workbench.aivia.asia/chat/lOMVPbz7rZmbJSJl 可对话
[ ] 一句话要课件仍有 DOWNLOAD_READY / 可下载
[ ] 至少一条「非机房内网」网络路径验证（手机 4G 或异地）
[ ] Issue #1 留：「E1 PASS」+ 证书类型（LE DNS-01 / 云）
[ ] 更新 ops/DEBT-LEDGER.md · upstream/PIN.md · ops/INFRA.md
```

## 禁止

- 密钥 / AK / IP 进仓  
- `nginx -s stop` 不恢复  
- E1 未过勾 CLAIM-A/B  
- 借机开 C / 重刷 B  

## 勾选

见 `ops/E1-RUNBOOK.md`。
