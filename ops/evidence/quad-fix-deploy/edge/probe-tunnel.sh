#!/usr/bin/env bash
# Run on dmit (or any host that can reach 127.0.0.1:13080 tunnel)
set -euo pipefail
code=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 \
  -H 'Host: workbench.aivia.asia' \
  http://127.0.0.1:13080/chat/lOMVPbz7rZmbJSJl || echo 000)
echo "tunnel_chat_http=$code"
test "$code" = "200"
