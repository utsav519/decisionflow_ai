"""
FastAPI application entry point.

Registers routers, error handlers, and database startup.
"""

import logging
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.error_handlers import register_error_handlers
from app.core.logging import setup_logging
from app.db.init_db import check_database_health
from app.db.session import SessionLocal
from app.api.v1.ai import router as ai_router

settings = get_settings()
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DecisionFlow AI API",
    version="1.0.0",
    description="AI-assisted configurable decision automation platform.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Correlation-ID"],
)

@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID") or f"cor_{uuid4().hex}"
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response

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
    return {"status": "healthy",
        "service": "decisionflow-api", 
        "app": settings.app_name
        }

@app.get("/ready")
def readiness_check() -> dict:
    from app.db.init_db import get_database_info
    db = SessionLocal()
    try:
        db_info = get_database_info(db)
        return {
            "status": "ready",
            "dependencies": {
                "database": "available",
                "database_type": "mysql",
                "rule_engine": "available",
            },
            "capabilities": {
                "policy_management": True,
                "rule_evaluation": True,
                "audit_trail": True,
                "analytics": True,
            },
        }
    finally:
        db.close()

from app.api.v1.policies import router as policies_router
from app.api.v1.config import router as config_router
from app.api.v1.evaluations import router as evaluations_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.audit import router as audit_router

try:
    from app.api.v1.system import router as system_router
    app.include_router(system_router)
except ImportError:
    pass

app.include_router(policies_router, prefix=settings.api_v1_prefix)
app.include_router(config_router, prefix=settings.api_v1_prefix)
app.include_router(evaluations_router, prefix=settings.api_v1_prefix)
app.include_router(analytics_router, prefix=settings.api_v1_prefix)
app.include_router(audit_router, prefix=settings.api_v1_prefix)
app.include_router(ai_router)
