#!/usr/bin/env bash
# F3: bridge smoke — exit 0 only if all checks pass
set -euo pipefail
BASE="${BRIDGE_BASE:-http://127.0.0.1:18090/bridge/v1}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -f /home/ops/.secrets/bridge.env ]]; then
  # shellcheck disable=SC1091
  set -a
  # shellcheck disable=SC1091
  source /home/ops/.secrets/bridge.env
  set +a
fi

pass=0
fail=0
note() { echo "[smoke] $*"; }
ok() { echo "[ok] $*"; pass=$((pass + 1)); }
bad() { echo "[FAIL] $*"; fail=$((fail + 1)); }

json_field() {
  python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get(sys.argv[1],""))' "$1"
}

# 1 health
code=$(curl -sS -o /tmp/br-health.json -w '%{http_code}' "$BASE/health" || true)
if [[ "$code" == "200" ]]; then ok "health 200"; else bad "health got $code"; fi

# 2 no token → /me 401
code=$(curl -sS -o /tmp/br-me.json -w '%{http_code}' "$BASE/me" || true)
if [[ "$code" == "401" ]]; then ok "me without token 401"; else bad "me expected 401 got $code"; fi

# 3 exchange teacher (with exchange token if set)
EX_HDR=()
EX_BODY='{"sub":"smoke-teacher","school_id":"school-demo","role":"teacher","name":"smoke"}'
if [[ -n "${BRIDGE_EXCHANGE_TOKEN:-}" ]]; then
  EX_HDR=(-H "X-Bridge-Exchange-Token: ${BRIDGE_EXCHANGE_TOKEN}")
fi
code=$(curl -sS -o /tmp/br-ex.json -w '%{http_code}' -X POST "$BASE/auth/exchange" \
  -H 'Content-Type: application/json' "${EX_HDR[@]}" -d "$EX_BODY" || true)
if [[ "$code" != "200" ]]; then
  bad "exchange got $code $(cat /tmp/br-ex.json 2>/dev/null | head -c 120)"
  TOK=""
else
  ok "exchange 200"
  TOK=$(python3 -c 'import json; print(json.load(open("/tmp/br-ex.json"))["access_token"])')
fi

# wrong exchange token (only if token configured)
if [[ -n "${BRIDGE_EXCHANGE_TOKEN:-}" ]]; then
  code=$(curl -sS -o /tmp/br-ex-bad.json -w '%{http_code}' -X POST "$BASE/auth/exchange" \
    -H 'Content-Type: application/json' -H 'X-Bridge-Exchange-Token: wrong' \
    -d '{"sub":"x","school_id":"school-demo","role":"teacher"}' || true)
  if [[ "$code" == "401" ]]; then ok "bad exchange token 401"; else bad "bad exchange expected 401 got $code"; fi
fi

if [[ -n "${TOK:-}" ]]; then
  # 3b /me school_id
  code=$(curl -sS -o /tmp/br-me2.json -w '%{http_code}' "$BASE/me" -H "Authorization: Bearer $TOK" || true)
  sid=$(python3 -c 'import json; print(json.load(open("/tmp/br-me2.json")).get("school_id",""))' 2>/dev/null || true)
  if [[ "$code" == "200" && "$sid" == "school-demo" ]]; then ok "me school_id"; else bad "me school $code $sid"; fi

  # 4 cross school 403
  code=$(curl -sS -o /tmp/br-cross.json -w '%{http_code}' \
    "$BASE/schools/school-other/classes" -H "Authorization: Bearer $TOK" || true)
  if [[ "$code" == "403" ]]; then ok "cross-school 403"; else bad "cross expected 403 got $code"; fi

  # 5 create proposal
  code=$(curl -sS -o /tmp/br-prop.json -w '%{http_code}' -X POST "$BASE/proposals" \
    -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' \
    -d '{"type":"lesson_plan_archive","title":"smoke-prop","note":"smoke"}' || true)
  status=$(python3 -c 'import json; print(json.load(open("/tmp/br-prop.json")).get("status",""))' 2>/dev/null || true)
  pid=$(python3 -c 'import json; print(json.load(open("/tmp/br-prop.json")).get("id",""))' 2>/dev/null || true)
  if [[ "$code" == "201" && "$status" == "pending_review" && -n "$pid" ]]; then
    ok "create_proposal pending"
  else
    bad "create_proposal $code $status"
  fi

  # 6 apply 403
  if [[ -n "$pid" ]]; then
    code=$(curl -sS -o /tmp/br-apply.json -w '%{http_code}' -X POST "$BASE/proposals/$pid/apply" \
      -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{}' || true)
    if [[ "$code" == "403" ]]; then ok "apply 403"; else bad "apply expected 403 got $code"; fi

    # 7 teacher review 403
    code=$(curl -sS -o /tmp/br-tr.json -w '%{http_code}' -X POST "$BASE/proposals/$pid/review" \
      -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' \
      -d '{"decision":"approved"}' || true)
    if [[ "$code" == "403" ]]; then ok "teacher review 403"; else bad "teacher review expected 403 got $code"; fi
  fi

  # admin review
  code=$(curl -sS -o /tmp/br-admin.json -w '%{http_code}' -X POST "$BASE/auth/exchange" \
    -H 'Content-Type: application/json' "${EX_HDR[@]}" \
    -d '{"sub":"smoke-admin","school_id":"school-demo","role":"school_admin"}' || true)
  ATOK=$(python3 -c 'import json; print(json.load(open("/tmp/br-admin.json")).get("access_token",""))' 2>/dev/null || true)
  if [[ -n "$ATOK" && -n "$pid" ]]; then
    code=$(curl -sS -o /tmp/br-rev.json -w '%{http_code}' -X POST "$BASE/proposals/$pid/review" \
      -H "Authorization: Bearer $ATOK" -H 'Content-Type: application/json' \
      -d '{"decision":"rejected","note":"smoke"}' || true)
    st=$(python3 -c 'import json; print(json.load(open("/tmp/br-rev.json")).get("status",""))' 2>/dev/null || true)
    if [[ "$code" == "200" && "$st" == "rejected" ]]; then ok "admin review"; else bad "admin review $code $st"; fi
  else
    bad "admin exchange/token"
  fi
fi

# 8 expired token 401
if [[ -n "${BRIDGE_JWT_SECRET:-}" ]]; then
  code=$(python3 - <<'PY'
import jwt, time, urllib.request, urllib.error, os
secret=os.environ["BRIDGE_JWT_SECRET"]
tok=jwt.encode({"sub":"x","school_id":"school-demo","role":"teacher","iss":"bridge-mock","exp":int(time.time())-30}, secret, algorithm="HS256")
base=os.environ.get("BRIDGE_BASE","http://127.0.0.1:18090/bridge/v1")
req=urllib.request.Request(base+"/me", headers={"Authorization":f"Bearer {tok}"})
try:
  urllib.request.urlopen(req, timeout=5)
  print(200)
except urllib.error.HTTPError as e:
  print(e.code)
PY
)
  if [[ "$code" == "401" ]]; then ok "expired token 401"; else bad "expired expected 401 got $code"; fi
fi

note "pass=$pass fail=$fail"
if [[ "$fail" -gt 0 ]]; then
  exit 1
fi
exit 0
