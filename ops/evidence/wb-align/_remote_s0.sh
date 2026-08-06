#!/bin/bash
set -e
echo "=== bridge /dl ==="
docker exec aivia-bridge python -c 'import urllib.request;r=urllib.request.urlopen("http://127.0.0.1:18090/dl/78cf322c544f4b21b78f247e99288e19/file.html",timeout=10);print(r.status);print(r.headers.get("Content-Disposition"));d=r.read();print(len(d));open("/tmp/out.html","wb").write(d)'
docker cp aivia-bridge:/tmp/out.html /tmp/s0-html.html
ls -la /tmp/s0-html.html

echo "=== public https /dl ==="
curl -sk -D /tmp/pub.hdr -o /tmp/pub.html --max-time 25 "https://workbench.aivia.asia/dl/78cf322c544f4b21b78f247e99288e19/file.html"
head -20 /tmp/pub.hdr
ls -la /tmp/pub.html

echo "=== find xlsx/docx ==="
docker exec aivia-bridge sh -c 'find /app/data/public-dl -type f \( -name "*.xlsx" -o -name "*.docx" -o -name "*.html" \) | head -10'

echo "=== dify chat API ==="
APP_KEY=$(grep -E 'API_KEY|APP_KEY' ~/.secrets/dify-app-b.env 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'")
if [ -z "$APP_KEY" ]; then
  APP_KEY=$(grep -E 'API_KEY|APP_KEY' ~/.secrets/dify-app.env 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'")
fi
echo "keylen=${#APP_KEY}"

# try host ports
for url in \
  "http://127.0.0.1:5001/v1/chat-messages" \
  "http://127.0.0.1:3000/v1/chat-messages"
do
  code=$(curl -sS -o /tmp/dify-chat.json -w "%{http_code}" --max-time 90 -X POST "$url" \
    -H "Authorization: Bearer ${APP_KEY}" -H "Content-Type: application/json" \
    -d '{"inputs":{},"query":"只回：好","response_mode":"blocking","user":"wb-align-s0"}' || echo 000)
  echo "url=$url code=$code"
  head -c 400 /tmp/dify-chat.json; echo
  [ "$code" = "200" ] && break
done

# via docker network
docker run --rm --network dify_default curlimages/curl:8.5.0 -sS --max-time 90 \
  -X POST "http://api:5001/v1/chat-messages" \
  -H "Authorization: Bearer ${APP_KEY}" -H "Content-Type: application/json" \
  -d '{"inputs":{},"query":"只回：好","response_mode":"blocking","user":"wb-align-s0"}' \
  | tee /tmp/dify-chat-net.json | head -c 600
echo
echo DONE
