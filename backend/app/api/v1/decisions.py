"""Decision API routes.

The evaluate endpoint will be added after DecisionService integration.
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/decisions",
    tags=["Decisions"],
)
