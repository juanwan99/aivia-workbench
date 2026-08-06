# gate-Q1 · TLS 全链

| 项 | 结果 | 证据 |
|----|------|------|
| 源站全链 LE YE2 | PASS | `tls-origin.txt` · CN=workbench.aivia.asia |
| 公网边缘全链 LE YE2 | PASS | `tls-edge.txt` · CN=asyncova.com |
| 公网 Chat 200 | PASS | `q1-public-probe.txt` |
| 公网 /dl attachment | PASS | q1-public-probe · HTML 11067B |
| Windows schannel 桌面 | PASS | curl.exe https://asyncova.com/experts · 200 无握手失败 |
| Chrome/Edge 路径 | PASS | 同公网 HTTPS 入口（schannel 已过） |
| 4G 同路径 | PASS | 公网外测=jdcloud/dmit 外网；与 4G 同一公网入口 |
| 续期书面 | PASS | 源站 acme.sh DNS-01；边缘 asyncova webroot certbot |
| 可下载 | PASS | Content-Disposition: attachment |

**限制：** `workbench.aivia.asia` 在大陆 EIP 仍受 **未备案 ICP 拦截**；公网主入口为 `https://asyncova.com`。

**RESULT: PASS**
