<<<<<<< HEAD
"""Central FastAPI error-handler registration.

Concrete domain exception mappings will be added after backend integration.
"""

from fastapi import FastAPI


def register_error_handlers(app: FastAPI) -> None:
    """Register shared application error handlers.

    Currently intentionally empty because backend domain exceptions have not
    yet been handed off.
    """
    return None
=======
"""
Global error handlers for FastAPI.

Catches ApplicationError, Pydantic validation errors, SQLAlchemy errors,
and unexpected exceptions. All return the contract error envelope.

Spec reference: §35 Global Error Handlers
"""

from __future__ import annotations

import logging
import traceback

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import ApplicationError

logger = logging.getLogger(__name__)


def register_error_handlers(app: FastAPI) -> None:
    """Register all global exception handlers on the FastAPI app."""

    @app.exception_handler(ApplicationError)
    async def application_error_handler(
        request: Request, exc: ApplicationError
    ) -> JSONResponse:
        """Handle known application errors."""
        correlation_id = request.headers.get(
            "x-correlation-id", "-"
        )
        logger.warning(
            "ApplicationError [%s]: %s (correlation=%s)",
            exc.code,
            exc.message,
            correlation_id,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                },
                "correlation_id": correlation_id,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def pydantic_validation_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle Pydantic request validation errors."""
        correlation_id = request.headers.get(
            "x-correlation-id", "-"
        )
        details = []
        for error in exc.errors():
            loc = ".".join(str(part) for part in error["loc"])
            details.append(
                {
                    "path": loc,
                    "issue": error["msg"],
                    "received": error.get("input"),
                }
            )
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "The request could not be processed.",
                    "details": details,
                },
                "correlation_id": correlation_id,
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handler(
        request: Request, exc: SQLAlchemyError
    ) -> JSONResponse:
        """Handle SQLAlchemy errors without exposing internals."""
        correlation_id = request.headers.get(
            "x-correlation-id", "-"
        )
        logger.error(
            "Database error (correlation=%s): %s",
            correlation_id,
            str(exc),
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": (
                        "A database error occurred. Please try again."
                    ),
                    "details": [],
                },
                "correlation_id": correlation_id,
            },
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle all unexpected errors with safe message."""
        correlation_id = request.headers.get(
            "x-correlation-id", "-"
        )
        logger.critical(
            "Unexpected error (correlation=%s): %s\n%s",
            correlation_id,
            str(exc),
            traceback.format_exc(),
        )
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": (
                        "An unexpected error occurred. "
                        "Please contact support."
                    ),
                    "details": [],
                },
                "correlation_id": correlation_id,
            },
        )
>>>>>>> origin/feature/backend-rule-engine
