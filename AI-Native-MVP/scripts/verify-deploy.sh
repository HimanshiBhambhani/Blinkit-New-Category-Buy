#!/usr/bin/env bash
# Post-deploy smoke tests — optionally pre-warms Render before checks.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

API_URL="${1:-}"
UI_URL="${2:-}"
STREAMLIT_URL="${3:-}"
SKIP_PREWARM="${SKIP_PREWARM:-0}"

if [[ -z "$API_URL" ]]; then
  echo "Usage: ./scripts/verify-deploy.sh <API_URL> [UI_URL] [STREAMLIT_URL]"
  echo "Example: ./scripts/verify-deploy.sh https://buy-smart-api.onrender.com https://ai-native-mvp.vercel.app https://grad-project-2ublqkxwzyxtpeczjt8zxi.streamlit.app"
  echo ""
  echo "Set SKIP_PREWARM=1 to skip Render cold-start retries."
  exit 1
fi

if [[ "$SKIP_PREWARM" != "1" ]]; then
  echo "==> Pre-warming Render (set SKIP_PREWARM=1 to skip)"
  "$SCRIPT_DIR/prewarm-render.sh" "$API_URL" 6 12
else
  echo "==> Skipping pre-warm (SKIP_PREWARM=1)"
fi

echo "==> API categories (smoke)"
curl -sf "$API_URL/api/trust/categories" | python3 -m json.tool | head -20

echo "==> boAt product trust"
curl -sf "$API_URL/api/trust/product/boat-airdopes-141" | python3 -m json.tool | head -20

echo "==> Electronics category"
curl -sf "$API_URL/api/trust/category/electronics" | python3 -m json.tool | head -15

if [[ -n "$UI_URL" ]]; then
  echo "==> UI homepage"
  code=$(curl -s -o /dev/null -w "%{http_code}" "$UI_URL/")
  echo "HTTP $code"
  if [[ "$code" != "200" ]]; then
    echo "WARNING: UI returned HTTP $code" >&2
  fi
fi

if [[ -n "$STREAMLIT_URL" ]]; then
  echo "==> Streamlit (Link A)"
  code=$(curl -s -o /dev/null -w "%{http_code}" "$STREAMLIT_URL/")
  echo "HTTP $code"
  if [[ "$code" != "200" ]]; then
    echo "WARNING: Streamlit returned HTTP $code" >&2
  fi
fi

echo "Done."
