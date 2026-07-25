# ──────────────────────────────────────────────────
# DecisionFlow AI — Backend Dockerfile
# Multi-stage build: slim Python 3.11 image
# ──────────────────────────────────────────────────

# Stage 1: Builder — install dependencies
FROM python:3.11-slim AS builder

WORKDIR /build

# Install system deps required by pymysql/cryptography
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libffi-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Runtime — lean production image
FROM python:3.11-slim AS runtime

LABEL maintainer="DecisionFlow Team"
LABEL description="DecisionFlow AI Backend — Rule-based decision engine"

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Own files by non-root user
RUN chown -R appuser:appuser /app

USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

ENTRYPOINT ["./entrypoint.sh"]
