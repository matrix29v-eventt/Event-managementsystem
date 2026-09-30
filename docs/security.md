# Security

## Decisions and where they are enforced

1. **No secrets in git.** Real values live only in `.env` (local), GitHub
   Secrets/Environments (CI/CD), or the operator's shell. `.env.example`
   contains names only. Ignored paths (root `.gitignore`): `.env`,
   `.env.staging`, `.env.prod`, `*.db`, `*.log`, `.last_good_image`, `.prev_image_tag`.
2. **Secret injection, not bake-in.** The image contains no credentials:
   the Dockerfile copies no `.env` (excluded by `.dockerignore`), and
   staging/prod Compose files inject `SECRET_KEY`, `POSTGRES_*`, and
   `DATABASE_URL` from the environment at deploy time. Required vars use
   `${VAR:?message}` so a missing secret fails fast instead of booting insecurely.
3. **JWT preserved.** HS256 via `SECRET_KEY`, 30-minute expiry default, bcrypt
   password hashes, `role_required("admin")` on mutating routes. CI smoke test
   asserts bad credentials get 401 and client tokens get 403 on admin routes.
4. **Minimal workflow permissions.** CI uses `contents: read`; CD adds only
   `packages: write` (GHCR push). Registry auth uses the ephemeral
   `secrets.GITHUB_TOKEN` — never a long-lived PAT in the repo.
5. **No credentials in logs.** Workflows pass secrets via `env:`, never `echo`;
   `deploy.sh` prints image refs and ports but never secret values.
6. **Least-privilege runtime.** API image runs as UID 10001 (`appuser`);
   Postgres runs its stock non-root entrypoint. No `privileged` containers,
   no Docker-socket mounts. Staging/prod restart policies (`unless-stopped` /
   `always`) recover crashed containers without human SSH access.
7. **Environment separation.** Distinct Compose projects, container names,
   volumes, and ports per environment (staging 8001 / prod-like 8002) so a
   staging deploy can never touch prod data.

## Honest limitations

- No TLS/HTTPS (local deployment; do not expose to the internet as-is).
- No secret rotation automation; no image vulnerability scanning in CI yet.
- `docker-compose.yml` (dev) keeps default-credential fallbacks for local
  convenience — staging/prod files require explicit secrets instead.
