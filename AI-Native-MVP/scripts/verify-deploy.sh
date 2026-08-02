#!/usr/bin/env bash
# Post-deploy smoke tests for Phase 6
set -euo pipefail

API_URL="${1:-}"
UI_URL="${2:-}"
STREAMLIT_URL="${3:-}"

if [[ -z "$API_URL" ]]; then
  echo "Usage: ./scripts/verify-deploy.sh <API_URL> [UI_URL] [STREAMLIT_URL]"
  echo "Example: ./scripts/verify-deploy.sh https://buy-smart-api.onrender.com https://buy-smart.vercel.app"
  exit 1
fi

echo "==> API health"
curl -sf "$API_URL/api/health" | python3 -m json.tool

echo "==> boAt product trust"
curl -sf "$API_URL/api/trust/product/boat-airdopes-141" | python3 -m json.tool | head -20

echo "==> Electronics category"
curl -sf "$API_URL/api/trust/category/electronics" | python3 -m json.tool | head -15

if [[ -n "$UI_URL" ]]; then
  echo "==> UI homepage"
  code=$(curl -s -o /dev/null -w "%{http_code}" "$UI_URL/")
  echo "HTTP $code"
fi

if [[ -n "$STREAMLIT_URL" ]]; then
  echo "==> Streamlit (Link A)"
  code=$(curl -s -o /dev/null -w "%{http_code}" "$STREAMLIT_URL/")
  echo "HTTP $code"
fi

echo "Done."
