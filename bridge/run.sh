#!/usr/bin/env bash
# Start aivia-bridge. Secret required — never invent weak defaults for long-running deploys.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# defaults before secrets; systemd Environment= may pre-set MODE/HOST/EXTRA
export BRIDGE_MODE="${BRIDGE_MODE:-hybrid}"
export BRIDGE_HOST="${BRIDGE_HOST:-0.0.0.0}"
export BRIDGE_PORT="${BRIDGE_PORT:-18090}"
export BRIDGE_EXTRA_HOSTS="${BRIDGE_EXTRA_HOSTS:-}"

if [[ -f /home/ops/.secrets/bridge.env ]]; then
  # shellcheck disable=SC1091
  set -a
  # shellcheck disable=SC1091
  source /home/ops/.secrets/bridge.env
  set +a
fi

# re-apply intentional deploy defaults after env file (env file must not force mock forever)
export BRIDGE_MODE="${BRIDGE_MODE:-hybrid}"
export BRIDGE_HOST="${BRIDGE_HOST:-0.0.0.0}"
export BRIDGE_PORT="${BRIDGE_PORT:-18090}"
export BRIDGE_EXTRA_HOSTS="${BRIDGE_EXTRA_HOSTS:-}"
export BRIDGE_JWT_ISS="${BRIDGE_JWT_ISS:-bridge-hybrid}"

if [[ -z "${BRIDGE_JWT_SECRET:-}" ]]; then
  echo "[aivia-bridge] FATAL: BRIDGE_JWT_SECRET not set. Put it in ~/.secrets/bridge.env" >&2
  exit 2
fi

export BRIDGE_JWT_SECRET
export BRIDGE_EXCHANGE_TOKEN="${BRIDGE_EXCHANGE_TOKEN:-}"
export BRIDGE_DATA_DIR="${BRIDGE_DATA_DIR:-$ROOT/bridge/data}"
mkdir -p "$BRIDGE_DATA_DIR"
exec python3 "$ROOT/bridge/server.py"
