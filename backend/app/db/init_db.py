"""
Database initialization and health check utilities.

Spec reference: §50 Health and Readiness Support
"""

import logging

from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def check_database_health(db: Session) -> bool:
    """Verify MySQL is reachable and responsive.

    Args:
        db: Active SQLAlchemy session.

    Returns:
        True if the database responds to a simple query.
    """
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.error("Database health check failed: %s", str(exc))
        return False


def get_database_info(db: Session) -> dict:
    """Return database metadata for readiness endpoints.

    Args:
        db: Active SQLAlchemy session.

    Returns:
        Dict with database type, version, and status.
    """
    try:
        result = db.execute(text("SELECT VERSION()"))
        version = result.scalar()
        return {
            "status": "available",
            "database_type": "mysql",
            "version": version,
        }
    except Exception as exc:
        logger.error("Failed to get database info: %s", str(exc))
        return {
            "status": "unavailable",
            "database_type": "mysql",
            "version": None,
        }
