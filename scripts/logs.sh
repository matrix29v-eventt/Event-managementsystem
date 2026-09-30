#!/usr/bin/env bash
# Convenience log viewer for the Compose stacks.
#
# Usage: ./scripts/logs.sh [staging|prod|dev] [api|db|all] [--follow]
# Examples:
#   ./scripts/logs.sh staging api
#   ./scripts/logs.sh prod all --follow
#   ./scripts/logs.sh staging api --follow
set -euo pipefail

ENVIRONMENT="${1:-staging}"
SERVICE="${2:-all}"
FOLLOW="${3:-}"

case "$ENVIRONMENT" in
  staging) COMPOSE_FILE="docker-compose.staging.yml" ;;
  prod)    COMPOSE_FILE="docker-compose.prod.yml" ;;
  dev)     COMPOSE_FILE="docker-compose.yml" ;;
  *) echo "Usage: $0 [staging|prod|dev] [api|db|all] [--follow]" >&2; exit 2 ;;
esac

# Normalise service alias to the Compose service name.
case "$SERVICE" in
  api) TARGET="api" ;;
  db)  TARGET="postgres_db" ;;
  all) TARGET="" ;;
  *) echo "Unknown service '$SERVICE' (use api|db|all)" >&2; exit 2 ;;
esac
# Dev stack names its backend service "backend", not "api".
if [ "$ENVIRONMENT" = "dev" ] && [ "$TARGET" = "api" ]; then TARGET="backend"; fi

# Log viewing must not require deployment secrets: fall back to a dummy tag so
# Compose interpolation succeeds (logs never pull or start images).
export IMAGE_TAG="${IMAGE_TAG:-ems-api:local}"

if [ "$FOLLOW" = "--follow" ] || [ "$FOLLOW" = "-f" ]; then
  # shellcheck disable=SC2086
  docker compose -f "$COMPOSE_FILE" logs -f --tail=100 $TARGET
else
  # shellcheck disable=SC2086
  docker compose -f "$COMPOSE_FILE" logs --tail=100 $TARGET
  if [ "$SERVICE" = "all" ]; then
    echo "--- container health ---"
    docker compose -f "$COMPOSE_FILE" ps
  fi
fi
