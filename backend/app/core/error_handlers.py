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
