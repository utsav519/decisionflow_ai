"""
Structured logging configuration with correlation ID support.

Spec reference: §38 Logging
"""

import logging
import sys
from typing import Any


class CorrelationLogAdapter(logging.LoggerAdapter):
    """Logger adapter that injects correlation_id into all log records."""

    def process(
        self, msg: str, kwargs: dict[str, Any]
    ) -> tuple[str, dict[str, Any]]:
        correlation_id = self.extra.get("correlation_id", "-")
        return f"[{correlation_id}] {msg}", kwargs


def setup_logging(level: str = "INFO") -> None:
    """Configure application-wide logging.

    Args:
        level: Log level string (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    log_format = (
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=log_format,
        datefmt="%Y-%m-%dT%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    # Suppress noisy third-party loggers
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("alembic").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)


def get_logger(
    name: str, correlation_id: str = "-"
) -> CorrelationLogAdapter:
    """Get a logger with correlation ID context.

    Args:
        name: Logger name (typically __name__).
        correlation_id: Request correlation ID.

    Returns:
        Logger adapter with correlation context.
    """
    logger = logging.getLogger(name)
    return CorrelationLogAdapter(
        logger, {"correlation_id": correlation_id}
    )
