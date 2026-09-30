#!/usr/bin/env bash
# Idempotent environment deployment with health gating and failure detection.
#
# Usage: IMAGE_TAG=<image> ./scripts/deploy.sh [staging|prod]
#   APP_PORT  host port for the API (default 8001 staging / 8002 prod)
#   APP_HOST  host for probes (default localhost)
#
# Flow: validate -> record previous image -> pull -> up -> wait /health ->
#       smoke test -> record last-good. On failure: dump logs, auto-restore the
#       previous image when one exists, exit 1.
set -euo pipefail

ENVIRONMENT="${1:-staging}"
case "$ENVIRONMENT" in
  staging) COMPOSE_FILE="docker-compose.staging.yml"; DEFAULT_PORT="8001" ;;
  prod)    COMPOSE_FILE="docker-compose.prod.yml";     DEFAULT_PORT="8002" ;;
  *) echo "Usage: $0 [staging|prod]" >&2; exit 2 ;;
esac

APP_PORT="${APP_PORT:-$DEFAULT_PORT}"
APP_HOST="${APP_HOST:-localhost}"
BASE_URL="http://${APP_HOST}:${APP_PORT}"
export APP_PORT

: "${IMAGE_TAG:?IMAGE_TAG is required (e.g. ghcr.io/<owner>/<repo>/ems-api:<sha>)}"
: "${POSTGRES_USER:?POSTGRES_USER is required}"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is required}"
: "${SECRET_KEY:?SECRET_KEY is required}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "$REPO_ROOT"

PREV_FILE=".prev_image_tag"
GOOD_FILE=".last_good_image"
HEALTH_TIMEOUT="${HEALTH_TIMEOUT:-120}"

echo "==> Deploying [${ENVIRONMENT}] with image ${IMAGE_TAG} on port ${APP_PORT}"

# Remember the currently running image so a failed deploy can restore it.
PREVIOUS_IMAGE=""
if docker compose -f "$COMPOSE_FILE" ps -q api >/dev/null 2>&1; then
  PREVIOUS_IMAGE="$(docker inspect --format='{{.Config.Image}}' \
    "$(docker compose -f "$COMPOSE_FILE" ps -q api 2>/dev/null)" 2>/dev/null || true)"
  if [ -n "$PREVIOUS_IMAGE" ] && [ "$PREVIOUS_IMAGE" != "$IMAGE_TAG" ]; then
    echo "$PREVIOUS_IMAGE" > "$PREV_FILE"
    echo "==> Recorded previous image: ${PREVIOUS_IMAGE}"
  fi
fi

# Pull the requested image. Local-only tags have nothing to pull — warn and continue.
echo "==> Pulling image ${IMAGE_TAG}"
if ! docker pull "$IMAGE_TAG"; then
  echo "==> WARNING: could not pull ${IMAGE_TAG}; continuing with local image (local fallback)"
fi

echo "==> Starting services (${COMPOSE_FILE})"
IMAGE_TAG="$IMAGE_TAG" docker compose -f "$COMPOSE_FILE" up -d

fail_deploy() {
  echo "==> DEPLOYMENT FAILED: $1" >&2
  echo "==> --- api logs (tail 100) ---" >&2
  docker compose -f "$COMPOSE_FILE" logs --tail=100 api >&2 || true
  echo "==> --- db logs (tail 30) ---" >&2
  docker compose -f "$COMPOSE_FILE" logs --tail=30 postgres_db >&2 || true
  if [ -n "$PREVIOUS_IMAGE" ] && [ "$PREVIOUS_IMAGE" != "$IMAGE_TAG" ]; then
    echo "==> Attempting automatic restore of previous image ${PREVIOUS_IMAGE}" >&2
    if IMAGE_TAG="$PREVIOUS_IMAGE" docker compose -f "$COMPOSE_FILE" up -d; then
      echo "==> Previous image restored (verify with scripts/smoke_test.sh)" >&2
    else
      echo "==> Automatic restore also failed — manual action required" >&2
    fi
  fi
  exit 1
}

# Wait for liveness.
echo "==> Waiting for ${BASE_URL}/health (timeout ${HEALTH_TIMEOUT}s)"
elapsed=0
until curl -sf "${BASE_URL}/health" >/dev/null 2>&1; do
  if [ "$elapsed" -ge "$HEALTH_TIMEOUT" ]; then
    fail_deploy "health check did not pass within ${HEALTH_TIMEOUT}s"
  fi
  sleep 5
  elapsed=$((elapsed + 5))
  echo "    ... waiting (${elapsed}s)"
done
echo "==> Health check passed"

# Full smoke suite gates success.
APP_PORT="$APP_PORT" bash scripts/smoke_test.sh "$BASE_URL" \
  || fail_deploy "smoke tests failed"

echo "$IMAGE_TAG" > "$GOOD_FILE"
echo "==> DEPLOYMENT SUCCESS: [${ENVIRONMENT}] ${IMAGE_TAG} (recorded in ${GOOD_FILE})"
