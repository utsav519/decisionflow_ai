"""
Policy version ORM model (immutable snapshots).

Spec reference: §11.2 Policy version model
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PolicyVersion(Base):
    """Immutable snapshot of a policy at a point in time."""

    __tablename__ = "policy_versions"

    id: Mapped[str] = mapped_column(
        String(40), primary_key=True
    )
    policy_id: Mapped[str] = mapped_column(
        String(40), nullable=False, index=True
    )
    version: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(120), nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    domain: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    status_snapshot: Mapped[str] = mapped_column(
        String(30), nullable=False
    )
    priority: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    decision: Mapped[str] = mapped_column(
        String(30), nullable=False
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

    __table_args__ = (
        UniqueConstraint(
            "policy_id",
            "version",
            name="uq_policy_version",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<PolicyVersion policy_id={self.policy_id} "
            f"version={self.version}>"
        )
