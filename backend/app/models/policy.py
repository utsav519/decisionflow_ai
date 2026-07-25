"""
Policy ORM model.

Spec reference: §11.1 Policy model
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Policy(Base):
    """Represents a business rule policy stored in MySQL."""

    __tablename__ = "policies"

    id: Mapped[str] = mapped_column(
        String(40), primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    domain: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(30), nullable=False, index=True
    )
    priority: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )
    decision: Mapped[str] = mapped_column(
        String(30), nullable=False, index=True
    )
    conditions_json: Mapped[dict] = mapped_column(
        JSON, nullable=False
    )
    reason: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    source: Mapped[str] = mapped_column(
        String(30), nullable=False
    )
    current_version: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1
    )
    ai_metadata_json: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )
    created_by: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    approved_by: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    activated_at: Mapped[datetime | None] = mapped_column(
        DateTime(), nullable=True
    )
    disabled_at: Mapped[datetime | None] = mapped_column(
        DateTime(), nullable=True
    )

    __table_args__ = (
        Index("ix_policies_domain_status", "domain", "status"),
    )

    def __repr__(self) -> str:
        return (
            f"<Policy id={self.id} name={self.name!r} "
            f"status={self.status}>"
        )
