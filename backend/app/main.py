"""
FastAPI application entry point.

Registers routers, error handlers, and database startup.
The integration lead is the final owner of application wiring;
the backend engineer registers only backend-owned routers.

Spec reference: §5 Repository Ownership (main.py notes)
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.error_handlers import register_error_handlers
from app.core.logging import setup_logging
from app.db.init_db import check_database_health
from app.db.session import SessionLocal

settings = get_settings()

# Configure logging before app creation
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register global error handlers
register_error_handlers(app)


@app.on_event("startup")
def startup_event() -> None:
    """Verify database connectivity on startup."""
    logger.info("Starting %s (%s)", settings.app_name, settings.app_env)
    db = SessionLocal()
    try:
        healthy = check_database_health(db)
        if healthy:
            logger.info("Database connection: healthy")
        else:
            logger.error("Database connection: unhealthy")
    finally:
        db.close()


@app.get("/health")
def health_check() -> dict:
    """Basic health check endpoint."""
    return {"status": "ok", "app": settings.app_name}


@app.get("/ready")
def readiness_check() -> dict:
    """Readiness check with dependency status."""
    from app.db.init_db import get_database_info

    db = SessionLocal()
    try:
        db_info = get_database_info(db)
        return {
            "status": "ready" if db_info["status"] == "available" else "not_ready",
            "dependencies": {
                "database": db_info["status"],
                "database_type": db_info["database_type"],
                "rule_engine": "available",
            },
        }
    finally:
        db.close()


# ------------------------------------------------------------------
# Router registration
# ------------------------------------------------------------------
from app.api.v1.policies import router as policies_router
from app.api.v1.config import router as config_router
from app.api.v1.evaluations import router as evaluations_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.audit import router as audit_router

app.include_router(policies_router, prefix=settings.api_v1_prefix)
app.include_router(config_router, prefix=settings.api_v1_prefix)
app.include_router(evaluations_router, prefix=settings.api_v1_prefix)
app.include_router(analytics_router, prefix=settings.api_v1_prefix)
app.include_router(audit_router, prefix=settings.api_v1_prefix)
