# FastAPI application image (used by base, staging and prod-like Compose stacks).
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies first so Docker layer caching reuses this step
# when only application code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root runtime user before copying code.
RUN useradd --create-home --uid 10001 appuser

COPY . .

# Writable locations the app/tests touch at runtime (SQLite fallback, pytest cache).
RUN mkdir -p /app/.pytest_cache && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Predictable production startup (no --reload; Compose base file may override for dev).
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
