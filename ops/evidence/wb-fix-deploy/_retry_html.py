#!/usr/bin/env python3
import json, re, urllib.request, subprocess, time
from pathlib import Path

print("FAILED head:")
p = Path("/tmp/wb-fix-deploy-f12/list_html.answer.txt")
print(p.read_text(encoding="utf-8")[:1500] if p.exists() else "missing")

TOK = Path("/tmp/wb-align-app-key.txt").read_text().strip()
IP = (
    subprocess.check_output(
        [
            "docker",
            "inspect",
            "dify-api-1",
            "--format",
            "{{range .NetworkSettings.Networks}}{{.IPAddress}} {{end}}",
        ],
        text=True,
    )
    .strip()
    .split()[0]
)
BASE = f"http://{IP}:5001/v1"
payload = json.dumps(
    {
        "inputs": {},
        "query": "请生成一份初中数学《一次函数》HTML课件，必须给出交付文件 html 和可下载链接。",
        "response_mode": "blocking",
        "user": "wb-fix-html2",
    }
).encode()
req = urllib.request.Request(
    BASE + "/chat-messages",
    data=payload,
    headers={"Authorization": f"Bearer {TOK}", "Content-Type": "application/json"},
    method="POST",
)
t0 = time.time()
with urllib.request.urlopen(req, timeout=300) as resp:
    d = json.loads(resp.read().decode())
ans = d.get("answer") or ""
Path("/tmp/wb-fix-deploy-f12/list_html2.answer.txt").write_text(ans, encoding="utf-8")
links = re.findall(r"https://workbench\.aivia\.asia/dl/[^\s\)]+", ans)
print(
    "elapsed",
    round(time.time() - t0, 1),
    "len",
    len(ans),
    "links",
    links[:2],
    "has_list",
    "## 交付清单" in ans,
    "DOWNLOAD",
    "DOWNLOAD_READY" in ans,
)
print(ans[:500])
if links:
    m = re.search(r"/dl/([a-f0-9]+)/([^?\s]+)", links[0])
    fid, name = m.group(1), m.group(2)
    subprocess.check_call(
        "docker exec aivia-bridge python -c "
        f"\"import urllib.request;open('/tmp/art','wb').write(urllib.request.urlopen('http://127.0.0.1:18090/dl/{fid}/{name}',timeout=30).read())\"",
        shell=True,
    )
    subprocess.check_call(
        "docker cp aivia-bridge:/tmp/art /tmp/wb-fix-deploy-f12/list_html2.html",
        shell=True,
    )
    print("html_size", Path("/tmp/wb-fix-deploy-f12/list_html2.html").stat().st_size)
