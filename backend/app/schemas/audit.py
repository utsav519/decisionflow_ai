"""
Audit log schemas.

Spec reference: §30 Audit & Traceability
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: str
    action: str
    entity_type: str
    entity_id: str
    entity_version: int | None
    performed_by: str | None
    summary: str
    request_snapshot: dict[str, Any] | None
    result_snapshot: dict[str, Any] | None
    metadata: dict[str, Any] | None
    correlation_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuditLogListItem(BaseModel):
    id: str
    action: str
    entity_type: str
    entity_id: str
    performed_by: str | None
    summary: str
    correlation_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
