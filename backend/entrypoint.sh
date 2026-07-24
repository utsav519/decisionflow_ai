#!/bin/bash
set -e

echo "╔══════════════════════════════════════════╗"
echo "║  DecisionFlow AI Backend — Starting...   ║"
echo "╚══════════════════════════════════════════╝"

# ─── Step 1: Wait for MySQL ─────────────────────────
echo "[1/4] Waiting for MySQL to accept connections..."
MAX_RETRIES=30
RETRY_COUNT=0
until python -c "
from app.core.config import get_settings
from sqlalchemy import create_engine, text
s = get_settings()
e = create_engine(s.database_url)
with e.connect() as c:
    c.execute(text('SELECT 1'))
print('MySQL is ready.')
" 2>/dev/null; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "ERROR: MySQL did not become ready after $MAX_RETRIES retries."
        exit 1
    fi
    echo "  Waiting for MySQL... (attempt $RETRY_COUNT/$MAX_RETRIES)"
    sleep 2
done

# ─── Step 2: Run Alembic Migrations ─────────────────
echo "[2/4] Running database migrations..."
python -m alembic upgrade head
echo "  Migrations applied."

# ─── Step 3: Seed Data ──────────────────────────────
echo "[3/4] Seeding database..."
python -c "
from app.db.seed import seed_policies
from app.db.session import SessionLocal
db = SessionLocal()
try:
    count = seed_policies(db)
    print(f'  Seeded {count} new policies.')
finally:
    db.close()
"

# ─── Step 4: Start Uvicorn ──────────────────────────
echo "[4/4] Starting Uvicorn server..."
echo ""
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers "${UVICORN_WORKERS:-1}" \
    --log-level "${LOG_LEVEL:-info}" \
    --access-log
