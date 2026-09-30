# Failure scenarios

How each failure is detected, what causes it, and how to recover.
Reproduce each one locally before claiming it in an interview.

## 1. Test failure
- **Symptom:** CI `validate-and-test` job goes red.
- **Detection:** `pytest -q` exits non-zero; `docker-build` job is skipped (`needs:`).
- **Likely cause:** broken logic, bad fixture, missing env (`DATABASE_URL`/`SECRET_KEY`).
- **Recovery:** fix code, push; broken code can never become an image.
- **Reproduce:** change an assertion in `tests/test_health.py`, run `pytest`.

## 2. Docker build failure
- **Symptom:** CI `docker-build` job fails; CD `publish` job fails.
- **Detection:** `docker/build-push-action` non-zero exit; no image pushed.
- **Likely cause:** bad `requirements.txt` pin, syntax error surviving compileall, base image pull issue.
- **Recovery:** fix Dockerfile/requirements, re-run workflow. Previous images stay untouched.
- **Reproduce:** add a bogus package to `requirements.txt`, run `docker build ./event-management-system`.

## 3. Application startup failure (bad config / bad image)
- **Symptom:** `api` container restarts or exits; `/health` never answers.
- **Detection:** `deploy.sh` health-wait loop hits `HEALTH_TIMEOUT` → exit 1; Compose `healthcheck` stays `starting`/`unhealthy`.
- **Likely cause:** missing `SECRET_KEY` (Compose `${VAR:?}` fails fast), bad `DATABASE_URL`, exception at import.
- **Recovery:** `deploy.sh` auto-restores the previous image when one is recorded; otherwise `scripts/rollback.sh`.
- **Reproduce:** `SECRET_KEY= POSTGRES_PASSWORD=x IMAGE_TAG=<good> ./scripts/deploy.sh staging` and watch it fail fast.

## 4. Health check failure after start ("container up, app down")
- **Symptom:** container `running` but `/health` never returns 200.
- **Detection:** same health-wait timeout in `deploy.sh`; `docker compose ps` shows `unhealthy`.
- **Likely cause:** app bound to wrong port, lifespan crash swallowed, routed through wrong `APP_PORT`.
- **Recovery:** logs via `scripts/logs.sh`, then rollback.
- **Reproduce:** deploy with `APP_PORT` pointing at nothing or an image whose CMD is wrong.

## 5. Database unavailable
- **Symptom:** `/health` passes but `/ready` returns `{"status": "not_ready"}`; smoke test fails at step 2.
- **Detection:** `smoke_test.sh` readiness gate; Postgres `pg_isready` healthcheck failing; API logs show connection errors.
- **Likely cause:** wrong `POSTGRES_*`, volume/permission issue, DB container OOM-killed.
- **Recovery:** `scripts/logs.sh staging db`, fix credentials/volume, `docker compose up -d` again. App needs no code change — readiness flips back automatically.
- **Reproduce:** stop only the DB (`docker compose -f docker-compose.staging.yml stop postgres_db`), then `curl localhost:8001/ready`.

## 6. Deployment failure (smoke test catches a bad release)
- **Symptom:** health passes, smoke step 3/4 fails (e.g. auth returns 500 instead of 401).
- **Detection:** `deploy.sh` runs the full `smoke_test.sh` suite and exits 1 with log tails.
- **Likely cause:** migration/code mismatch, broken auth config, CORS regression.
- **Recovery:** automatic restore of `.prev_image_tag` + manual `scripts/rollback.sh <tag>`; confirm with smoke test.
- **Reproduce:** deploy an image built from a branch with a deliberately failing endpoint, watch rollback restore the old tag.

## Rollback behaviour (all scenarios)
- `deploy.sh` records the pre-deploy image in `.prev_image_tag` and the successful image in `.last_good_image`.
- `scripts/rollback.sh [env] [tag]` resolves tag as CLI arg → `$IMAGE_TAG` → `.prev_image_tag` → `.last_good_image`, redeploys, re-runs health + smoke, and updates `.last_good_image`.
