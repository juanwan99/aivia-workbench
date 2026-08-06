#!/bin/bash
set -e
ENVF=~/.secrets/dify-session.env
TOKEN=$(python3 - <<'PY'
from pathlib import Path
for line in Path.home().joinpath(".secrets/dify-session.env").read_text(encoding="utf-8").splitlines():
    if line.startswith("__HOST-ACCESS_TOKEN="):
        print(line.split("=",1)[1].strip().strip('"').strip("'"))
        break
PY
)
echo "token_len=${#TOKEN}"
BASE="http://127.0.0.1:13080"
code=$(curl -sS -o /tmp/apps.json -w "%{http_code}" --max-time 30 \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "${BASE}/console/api/apps?page=1&limit=50" || echo 000)
echo "apps code=$code"
python3 - <<'PY'
import json
from pathlib import Path
raw=Path("/tmp/apps.json").read_text(encoding="utf-8",errors="replace")
print(raw[:300])
try:
  d=json.loads(raw)
except Exception as e:
  print("json fail", e); raise SystemExit(1)
items=d.get("data") or []
print("n", len(items))
for a in items[:20]:
  site=a.get("site") or {}
  print("-", a.get("name"), "id", str(a.get("id"))[:8], "mode", a.get("mode"), "code", site.get("access_token") or site.get("code") or site.get("app_base_url"))
PY

# get app API token for known app
APP_ID=$(python3 - <<'PY'
from pathlib import Path
for line in Path.home().joinpath(".secrets/dify-app-b.env").read_text(encoding="utf-8").splitlines():
    if "ID=" in line:
        print(line.split("=",1)[1].strip().strip('"')); break
PY
)
echo "app_id=$APP_ID"
# try list api keys
code=$(curl -sS -o /tmp/keys.json -w "%{http_code}" --max-time 30 \
  -H "Authorization: Bearer ${TOKEN}" \
  "${BASE}/console/api/apps/${APP_ID}/api-keys" || echo 000)
echo "api-keys code=$code"
head -c 400 /tmp/keys.json; echo
