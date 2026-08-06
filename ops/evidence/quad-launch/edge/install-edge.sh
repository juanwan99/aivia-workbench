#!/bin/bash
# Install workbench edge locations into asyncova.com on dmit
set -euo pipefail
CONF=/etc/nginx/conf.d/asyncova.com.conf
INC=/etc/nginx/conf.d/asyncova-workbench-locations.inc
SRC_INC=/tmp/asyncova-workbench-locations.inc
BACKUP="/etc/nginx/conf.d/asyncova.com.conf.bak-quad-$(date +%Y%m%d%H%M%S)"

if [[ ! -f "$SRC_INC" ]]; then
  echo "missing $SRC_INC"
  exit 1
fi

sudo cp "$SRC_INC" "$INC"
sudo cp "$CONF" "$BACKUP"

# Inject include into SSL server block before "location /" if not already present
if grep -q 'asyncova-workbench-locations.inc' "$CONF"; then
  echo "include already present"
else
  sudo python3 - <<'PY'
from pathlib import Path
p = Path("/etc/nginx/conf.d/asyncova.com.conf")
text = p.read_text()
needle = "    location / {\n        try_files"
include_line = "    # QUAD-LAUNCH workbench edge\n    include /etc/nginx/conf.d/asyncova-workbench-locations.inc;\n\n"
if "asyncova-workbench-locations.inc" in text:
    print("already included")
else:
    if needle not in text:
        raise SystemExit("anchor location / not found")
    # Only first SSL server block occurrence after listen 127.0.0.1:8443
    idx = text.find("listen 127.0.0.1:8443 ssl;")
    if idx < 0:
        raise SystemExit("ssl listen not found")
    idx2 = text.find(needle, idx)
    if idx2 < 0:
        raise SystemExit("location / after ssl not found")
    text = text[:idx2] + include_line + text[idx2:]
    p.write_text(text)
    print("injected include")
PY
fi

sudo nginx -t
sudo systemctl reload nginx
echo "EDGE_INSTALL_OK backup=$BACKUP"
