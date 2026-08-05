#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export BRIDGE_MODE="${BRIDGE_MODE:-mock}"
export BRIDGE_HOST="${BRIDGE_HOST:-127.0.0.1}"
export BRIDGE_PORT="${BRIDGE_PORT:-18090}"
# secret only from env or local secrets file (not in git)
if [[ -z "${BRIDGE_JWT_SECRET:-}" && -f /home/ops/.secrets/bridge.env ]]; then
  # shellcheck disable=SC1091
  set -a
  # keys with safe names only
  source /home/ops/.secrets/bridge.env
  set +a
fi
export BRIDGE_JWT_SECRET="${BRIDGE_JWT_SECRET:-$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')}"
export BRIDGE_DATA_DIR="${BRIDGE_DATA_DIR:-$ROOT/bridge/data}"
mkdir -p "$BRIDGE_DATA_DIR"
exec python3 "$ROOT/bridge/server.py"
