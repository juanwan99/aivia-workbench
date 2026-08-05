#!/usr/bin/env bash
# Start aivia-bridge (mock). Secret required — never invent weak defaults for long-running deploys.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export BRIDGE_MODE="${BRIDGE_MODE:-mock}"
export BRIDGE_HOST="${BRIDGE_HOST:-127.0.0.1}"
export BRIDGE_PORT="${BRIDGE_PORT:-18090}"

if [[ -f /home/ops/.secrets/bridge.env ]]; then
  # shellcheck disable=SC1091
  set -a
  # shellcheck disable=SC1091
  source /home/ops/.secrets/bridge.env
  set +a
fi

if [[ -z "${BRIDGE_JWT_SECRET:-}" ]]; then
  echo "[aivia-bridge] FATAL: BRIDGE_JWT_SECRET not set. Put it in ~/.secrets/bridge.env" >&2
  exit 2
fi

export BRIDGE_JWT_SECRET
export BRIDGE_MODE
export BRIDGE_HOST
export BRIDGE_PORT
export BRIDGE_EXCHANGE_TOKEN="${BRIDGE_EXCHANGE_TOKEN:-}"
export BRIDGE_DATA_DIR="${BRIDGE_DATA_DIR:-$ROOT/bridge/data}"
mkdir -p "$BRIDGE_DATA_DIR"
exec python3 "$ROOT/bridge/server.py"
