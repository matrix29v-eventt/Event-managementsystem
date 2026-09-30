# SRE notes

## Concepts demonstrated (all implemented and testable)

- **Reliability as a pipeline property:** broken code cannot become an image —
  CI gates tests/lint before `docker-build` (`needs:`), CD deploys only images
  that passed CI on their branch.
- **Fault detection:** four layered gates — pytest, Docker build, Compose
  `healthcheck`, post-deploy smoke suite. Each layer catches what the previous
  one cannot (logic vs packaging vs runtime vs end-to-end behaviour).
- **Liveness vs readiness:** `GET /health` (process alive, no dependencies) vs
  `GET /ready` (request-scoped DB session via `get_db`, i.e. what a real request
  experiences). Compose, `deploy.sh`, and load-balancer-style probes each use
  the appropriate one.
- **Automated deployment:** `scripts/deploy.sh` is idempotent (re-running with
  the same tag converges), validates inputs, pulls, starts, waits, smoke-tests,
  and records the result — one command replaces a manual checklist.
- **Rollback / recovery:** previous image recorded before every deploy
  (`.prev_image_tag`); failure auto-restores it; `scripts/rollback.sh` restores
  any known-good SHA and re-verifies. Demonstrates *failed deployment → detect
  → recover* without orchestration magic.
- **Resilience:** `restart: unless-stopped` (staging) / `always` (prod-like),
  Postgres `pg_isready` gating so the API never boots against a dead DB,
  persistent named volumes so restarts keep data.
- **Observability (basic):** structured startup/request logs
  (`LOG_LEVEL`-controlled, `json-file` driver with rotation), `scripts/logs.sh`
  per service with follow mode, `docker compose ps` health column, `/health` +
  `/ready` as machine-readable signals.
- **Incident detection & error handling:** API returns typed errors
  (401/403/404/422 — covered by tests), smoke test asserts the auth layer
  rejects instead of 500ing, `docs/failure-scenarios.md` maps symptom →
  detection → cause → recovery for six scenarios.
- **Reducing manual intervention:** secrets via environment (never typed into
  files during deploy), floating `:staging`/`:latest` aliases updated by CI,
  last-good tag bookkeeping done by scripts.

## Explicitly NOT implemented

- True multi-region / multi-node HA (single Docker host).
- Kubernetes orchestration, Terraform/Ansible IaC.
- Production-scale monitoring (no Prometheus/Grafana; only health/readiness/logs).
- TLS termination, WAF, DDoS protection — do not expose this stack publicly as-is.
- Automated secret rotation, image CVE scanning, signed-image verification.
- Zero-downtime/blue-green deploys (brief restart window exists).
- Production traffic, SLOs/SLIs, paging/alerting.
