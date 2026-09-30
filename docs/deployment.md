# Deployment

## Environments

| Environment | Branch | Compose file | Default port | Registry tags |
|---|---|---|---|---|
| Local dev | any | `docker-compose.yml` | 8000 (+3000 UI) | local build |
| Staging | `develop` | `docker-compose.staging.yml` | 8001 | `:<sha>`, `:staging` |
| Production-like (local) | `main` | `docker-compose.prod.yml` | 8002 | `:<sha>`, `:latest` |

Production-like means: same image/tagging/health/smoke discipline as staging plus
prod safeguards (`restart: always`, stricter intervals, required `CORS_ORIGINS`,
`LOG_LEVEL=WARNING`), but still a single host with **no TLS and no HA**.

## Image tagging strategy

- **Primary: immutable commit SHA** — `ghcr.io/<owner>/<repo>/ems-api:<sha>`.
  CD deploys this exact digest-pinned-by-tag reference; SHA tags are never reused.
- **Floating aliases** — `:staging` and `:latest` mark the newest passing build per
  environment for human convenience only. Rollback and deploy scripts always use
  the SHA tag recorded in `.prev_image_tag` / `.last_good_image`.
- Never deploy `:latest` alone to production: it is not reproducible.
- All refs are lowercased by CI (`tr A-Z a-z`) because Docker/GHCR rejects
  uppercase in repository paths while `github.repository` preserves repo casing.

## Registry (GHCR) + local fallback

- CD logs in with `secrets.GITHUB_TOKEN` (`docker/login-action`), builds with
  `docker/build-push-action`, pushes SHA + alias tags.
- No registry available (e.g. fork without GHCR, offline laptop)? Build and
  deploy a local tag instead:
  `docker build -t ems-api:local ./event-management-system`, then
  `IMAGE_TAG=ems-api:local ./scripts/deploy.sh staging`.
  `deploy.sh` warns on pull failure and continues with the local image.

## Required configuration

Secrets per environment (GitHub Environment secrets in CI, shell env locally):

```text
IMAGE_TAG  POSTGRES_USER  POSTGRES_PASSWORD  POSTGRES_DB  SECRET_KEY
```

Plus for prod-like: `CORS_ORIGINS`. Optional: `ALGORITHM`,
`ACCESS_TOKEN_EXPIRE_MINUTES`, `LOG_LEVEL`, `APP_PORT`, `HEALTH_TIMEOUT`.

## Deploy / verify / recover commands

```bash
# staging (port 8001)
IMAGE_TAG=ghcr.io/<owner>/<repo>/ems-api:<sha> APP_PORT=8001 ./scripts/deploy.sh staging
./scripts/smoke_test.sh http://localhost:8001
./scripts/logs.sh staging api

# production-like (port 8002, manual gate via GitHub Environment)
IMAGE_TAG=ghcr.io/<owner>/<repo>/ems-api:<sha> APP_PORT=8002 ./scripts/deploy.sh prod

# rollback (auto-resolves last known-good tag)
./scripts/rollback.sh staging
./scripts/rollback.sh prod ghcr.io/<owner>/<repo>/ems-api:<previous-sha>
```

## Branching & release flow

```text
feature/* --PR--> CI (tests+lint+build) --merge--> develop
  --CD staging--> health+smoke --validate--> PR to main
  --merge--> CD production-like (manual approval) --> health+smoke
```

- CI runs on all PRs and pushes to `develop`/`main`.
- Staging deploys automatically on `develop` pushes; production deploys only from
  `main` and should have a required reviewer on the `production` environment.
- Feature branches never deploy anywhere.
