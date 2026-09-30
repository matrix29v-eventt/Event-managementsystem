#!/usr/bin/env bash
# Rollback an environment to a previous image tag.
#
# Usage: ./scripts/rollback.sh [staging|prod] [image_tag]
#   image_tag resolution order: CLI arg > $IMAGE_TAG env > .prev_image_tag >
#   .last_good_image. Refuses to run when nothing known-good is recorded.
set -euo pipefail

ENVIRONMENT="${1:-staging}"
case "$ENVIRONMENT" in
  staging) COMPOSE_FILE="docker-compose.staging.yml"; DEFAULT_PORT="8001" ;;
  prod)    COMPOSE_FILE="docker-compose.prod.yml";     DEFAULT_PORT="8002" ;;
  *) echo "Usage: $0 [staging|prod] [image_tag]" >&2; exit 2 ;;
esac

APP_PORT="${APP_PORT:-$DEFAULT_PORT}"
BASE_URL="http://localhost:${APP_PORT}"
export APP_PORT

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "$REPO_ROOT"

TARGET="${2:-${IMAGE_TAG:-}}"
if [ -z "$TARGET" ] && [ -f ".prev_image_tag" ]; then TARGET="$(cat .prev_image_tag)"; fi
if [ -z "$TARGET" ] && [ -f ".last_good_image" ]; then TARGET="$(cat .last_good_image)"; fi
if [ -z "$TARGET" ]; then
  echo "ERROR: no rollback target. Pass an image tag or ensure .prev_image_tag/.last_good_image exists." >&2
  exit 1
fi

echo "==> Rolling back [${ENVIRONMENT}] to ${TARGET}"
docker pull "$TARGET" || echo "==> WARNING: pull failed; continuing with local image"
IMAGE_TAG="$TARGET" docker compose -f "$COMPOSE_FILE" up -d

echo "==> Waiting for health after rollback"
elapsed=0
until curl -sf "${BASE_URL}/health" >/dev/null 2>&1; do
  if [ "$elapsed" -ge 120 ]; then
    echo "==> ROLLBACK FAILED: health check did not pass" >&2
    docker compose -f "$COMPOSE_FILE" logs --tail=100 api >&2 || true
    exit 1
  fi
  sleep 5
  elapsed=$((elapsed + 5))
done

APP_PORT="$APP_PORT" bash scripts/smoke_test.sh "$BASE_URL"
echo "$TARGET" > .last_good_image
echo "==> ROLLBACK SUCCESS: [${ENVIRONMENT}] now running ${TARGET}"
