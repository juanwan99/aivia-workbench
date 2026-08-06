#!/bin/bash
set -e
echo "=== secret files ==="
ls -la ~/.secrets/
echo "=== key names only ==="
for f in ~/.secrets/dify*.env; do
  echo "FILE=$f bytes=$(wc -c < "$f")"
  # print only variable names and value lengths
  while IFS= read -r line; do
    case "$line" in
      \#*|"") continue ;;
      *=*)
        k="${line%%=*}"
        v="${line#*=}"
        v="${v%\"}"; v="${v#\"}"; v="${v%\'}"; v="${v#\'}"
        echo "  $k len=${#v}"
        ;;
    esac
  done < "$f"
done

echo "=== docker api ports ==="
docker ps --format '{{.Names}} {{.Ports}}' | grep -iE 'api|nginx|web' || true
API_IP=$(docker inspect dify-api-1 --format '{{range .NetworkSettings.Networks}}{{.IPAddress}} {{end}}')
echo "api_ip=$API_IP"

# load first non-empty API key candidate
APP_KEY=""
for f in ~/.secrets/dify-app-b.env ~/.secrets/dify-app.env ~/.secrets/dify-session.env; do
  [ -f "$f" ] || continue
  while IFS= read -r line; do
    case "$line" in
      \#*|"") continue ;;
      *=*)
        k="${line%%=*}"; v="${line#*=}"
        v="${v%\"}"; v="${v#\"}"; v="${v%\'}"; v="${v#\'}"
        case "$k" in
          *API*|*KEY*|*TOKEN*|*APP*)
            if [ ${#v} -gt 10 ]; then APP_KEY="$v"; echo "picked from $f key=$k len=${#v}"; break 2; fi
            ;;
        esac
        ;;
    esac
  done < "$f"
done
echo "app_key_len=${#APP_KEY}"

if [ ${#APP_KEY} -lt 10 ]; then
  echo "NO_APP_KEY"; exit 2
fi

# hit API container IP
for base in "http://${API_IP%% *}:5001" "http://api:5001"; do
  echo "try $base"
done

# use docker network curl
docker run --rm --network container:dify-api-1 curlimages/curl:8.5.0 -sS --max-time 120 \
  -X POST "http://127.0.0.1:5001/v1/chat-messages" \
  -H "Authorization: Bearer ${APP_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"inputs":{},"query":"只回：好","response_mode":"blocking","user":"wb-align-s0"}' \
  | tee /tmp/dify-chat.json | head -c 800
echo
python3 - <<'PY'
import json
p="/tmp/dify-chat.json"
try:
  d=json.load(open(p,encoding="utf-8"))
  print("keys", list(d.keys())[:20])
  print("answer_head", str(d.get("answer",""))[:200])
except Exception as e:
  print("parse_fail", e)
  print(open(p,encoding="utf-8",errors="replace").read()[:500])
PY
