# 阶段 E1 · 正式证书 + 公网

```
STATUS: 执行窗 2026-08-06 · **E1 BLOCKED**（非取消）
门: CLAIM-A / CLAIM-B / 教师正式话术
```

> 按本文执行。**E1 未过禁止 CLAIM-B / 正式上线。** 勾选见 `ops/E1-RUNBOOK.md`。

## 为何 DNS-01

HTTP-01 外网 LE 校验 403 → 必须 DNS-01 或云证书。

## 路径甲 · certbot DNS-01 手工

```bash
sudo certbot certonly --manual --preferred-challenges dns \
  -d workbench.aivia.asia \
  --agree-tos -m admin@aivia.asia
# 阿里云 DNS 添加 _acme-challenge.workbench TXT
sudo nginx -t && sudo systemctl reload nginx
```

## 验收 E1 PASS

- [ ] 浏览器无证书警告  
- [ ] 默认 Chat 可聊  
- [ ] 课件可下载  
- [ ] 外网/4G 复验  
- [ ] Issue「E1 PASS」+ 更新 DEBT-LEDGER / PIN  

勾选：`ops/E1-RUNBOOK.md`。
