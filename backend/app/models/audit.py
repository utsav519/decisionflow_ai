"""
Audit log ORM model.

Append-only audit trail for all significant backend events.

Spec reference: §11.5 Audit model
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AuditLog(Base):
    """Append-only audit record for traceability."""

    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(
        String(40), primary_key=True
    )
    action: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )
    entity_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )
    entity_id: Mapped[str] = mapped_column(
        String(40), nullable=False, index=True
    )
    entity_version: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    performed_by: Mapped[str | None] = mapped_column(
        String(100), nullable=True, index=True
    )
    summary: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    request_snapshot_json: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )
    result_snapshot_json: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )
    metadata_json: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )
    correlation_id: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    def __repr__(self) -> str:
        return (
            f"<AuditLog id={self.id} action={self.action} "
            f"entity={self.entity_type}/{self.entity_id}>"
        )
