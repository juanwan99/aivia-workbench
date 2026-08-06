#!/usr/bin/env python3
import json, subprocess, urllib.request
from pathlib import Path
out = Path("/tmp/wb-fix-deploy-f0"); out.mkdir(exist_ok=True, parents=True)
# bridge health
h = subprocess.check_output(["docker","exec","aivia-bridge","python","-c","import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:18090/health',timeout=5).read().decode())"], text=True)
print("health", h.strip())
(out/"health.json").write_text(h.strip(), encoding="utf-8")
# container
meta = subprocess.check_output("docker inspect aivia-bridge --format '{{.Id}} {{.State.Status}} {{.Config.Image}}'", shell=True, text=True)
(out/"container.txt").write_text(meta, encoding="utf-8")
print("container", meta.strip())
# version in file
ver = subprocess.check_output("grep -n 'VERSION' /home/ops/aivia-workbench/bridge/server.py | head -3", shell=True, text=True)
(out/"server-version-grep.txt").write_text(ver, encoding="utf-8")
# /dl sample
dl = subprocess.check_output(["docker","exec","aivia-bridge","python","-c",
"import urllib.request;r=urllib.request.urlopen('http://127.0.0.1:18090/dl/78cf322c544f4b21b78f247e99288e19/file.html',timeout=10);print(r.status);print(r.headers.get('Content-Disposition'));print(len(r.read()))"], text=True)
(out/"dl-sample.txt").write_text(dl, encoding="utf-8")
print("dl", dl.strip())
# public https
import ssl
try:
  ctx=ssl.create_default_context()
  r=urllib.request.urlopen('https://workbench.aivia.asia/dl/78cf322c544f4b21b78f247e99288e19/file.html', timeout=20, context=ctx)
  pub=f"status={r.status} disp={r.headers.get('Content-Disposition')} len={len(r.read())}"
except Exception as e:
  pub=f"ERR {type(e).__name__}: {e}"
(out/"dl-public.txt").write_text(pub, encoding="utf-8")
print("public", pub)
# secrets not in repo path
sec = subprocess.check_output("ls -la ~/.secrets | head -20; test -f /home/ops/aivia-workbench/bridge/data/.env && echo BAD_ENV_IN_DATA || echo no_env_in_data", shell=True, text=True)
(out/"secrets-layout.txt").write_text(sec, encoding="utf-8")
# refuse write quick if api key exists
print("DONE", out)
