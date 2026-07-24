from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(tags=["System"])


@router.get("/health")
async def health() -> dict:
    """Process-level health check.

    This endpoint deliberately does not depend on MySQL or the AI provider.
    """
    return {
        "status": "healthy",
        "service": "decisionflow-api",
        "version": "0.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/ready")
async def readiness() -> dict:
    """Bootstrap readiness response.

    Replace these placeholders with real dependency checks after the
    backend and AI modules have been integrated.
    """
    return {
        "status": "degraded",
        "dependencies": {
            "database": "not_checked",
            "database_type": "mysql",
            "rule_engine": "not_integrated",
            "ai_provider": "not_integrated",
        },
        "capabilities": {
            "decision_evaluation": False,
            "ai_policy_generation": False,
            "ai_explanation": False,
        },
    }
