#!/usr/bin/env bash
# Post-deployment smoke test.
# Verifies "container started" actually means "application is healthy".
#
# Usage: ./scripts/smoke_test.sh [base_url]
#   base_url defaults to http://localhost:${APP_PORT:-8000}
#
# Checks:
#   1. GET /health  -> 200 {"status": "healthy"}
#   2. GET /ready   -> 200 {"status": "ready", "database": "connected"}
#   3. GET /        -> 200 (representative route: root API message)
#   4. POST /auth/token with bad credentials -> 401 (auth layer is up, not open)
# Exits non-zero on the first failure.
set -euo pipefail

BASE_URL="${1:-http://localhost:${APP_PORT:-8000}}"
echo "==> Smoke testing ${BASE_URL}"

pass() { echo "  [PASS] $1"; }
fail() { echo "  [FAIL] $1" >&2; exit 1; }

# 1. Liveness
HEALTH="$(curl -sf "${BASE_URL}/health")" || fail "GET /health unreachable or non-200"
echo "$HEALTH" | grep -q '"status"[[:space:]]*:[[:space:]]*"healthy"' \
  || fail "GET /health unexpected body: ${HEALTH}"
pass "GET /health -> 200 healthy"

# 2. Readiness (app + database)
READY="$(curl -sf "${BASE_URL}/ready")" || fail "GET /ready unreachable or non-200"
echo "$READY" | grep -q '"status"[[:space:]]*:[[:space:]]*"ready"' \
  || fail "GET /ready not ready: ${READY}"
echo "$READY" | grep -q '"database"[[:space:]]*:[[:space:]]*"connected"' \
  || fail "GET /ready database not connected: ${READY}"
pass "GET /ready -> 200 ready, database connected"

# 3. Representative route
ROOT="$(curl -sf "${BASE_URL}/")" || fail "GET / unreachable or non-200"
echo "$ROOT" | grep -q 'message' || fail "GET / unexpected body: ${ROOT}"
pass "GET / -> 200 API running"

# 4. Auth layer responds correctly (bad credentials must be rejected, not 500)
AUTH_CODE="$(curl -s -o /dev/null -w '%{http_code}' -X POST "${BASE_URL}/auth/token" \
  -H 'Content-Type: application/json' \
  -d '{"email":"smoke-test@example.com","password":"wrong-password"}')"
[ "$AUTH_CODE" = "401" ] || fail "POST /auth/token expected 401, got ${AUTH_CODE}"
pass "POST /auth/token -> 401 for bad credentials (auth enforced)"

echo "==> Smoke test SUCCESS: ${BASE_URL} is healthy"
