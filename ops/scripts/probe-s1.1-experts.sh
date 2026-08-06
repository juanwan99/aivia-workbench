#!/usr/bin/env bash
set -euo pipefail
BASE="${1:-https://asyncova.com}"
tmp="$(mktemp)"
code=$(curl -sS -o "$tmp" -w "%{http_code}" "$BASE/experts")
code2=$(curl -sS -o /dev/null -w "%{http_code}" "$BASE/experts/")
echo "HTTP /experts=$code /experts/=$code2"
ok=1
[[ "$code" == "200" && "$code2" == "200" ]] || ok=0
if grep -q '面向教师备课出件' "$tmp"; then
  echo "FAIL: still has 面向教师备课出件"
  ok=0
fi
if ! grep -q '通用' "$tmp"; then
  echo "FAIL: missing 通用"
  ok=0
fi
if ! grep -q '办公 Word' "$tmp"; then
  echo "FAIL: missing 办公 Word"
  ok=0
fi
if [[ "$ok" == "1" ]]; then
  echo "PASS: experts page general-wb copy"
  exit 0
fi
echo "FAIL"
exit 1
