#!/usr/bin/env bash
# Pre-warm Render free-tier API before demo / evaluation (cold start ~30–90s).
set -euo pipefail

API_URL="${1:-https://buy-smart-api.onrender.com}"
WARM_URL="${API_URL%/}/api/trust/categories"
MAX_ATTEMPTS="${2:-8}"
SLEEP_SECS="${3:-15}"

echo "==> Pre-warming Render API: $WARM_URL"
echo "    (up to $MAX_ATTEMPTS attempts, ${SLEEP_SECS}s apart)"

for ((i = 1; i <= MAX_ATTEMPTS; i++)); do
  if curl -sf --max-time 120 "$WARM_URL" >/dev/null; then
    echo "==> API warm after attempt $i"
    curl -sf "$WARM_URL" | python3 -m json.tool 2>/dev/null | head -20 || true
    exit 0
  fi
  echo "    attempt $i/$MAX_ATTEMPTS — not ready, sleeping ${SLEEP_SECS}s..."
  sleep "$SLEEP_SECS"
done

echo "ERROR: API did not respond after $MAX_ATTEMPTS attempts" >&2
exit 1
