"""
Evaluation ORM model.

Stores the result of evaluating customer data against active policies.

Spec reference: §11.3 Evaluation model
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


class Evaluation(Base):
    """Represents a single decision evaluation result."""

    __tablename__ = "evaluations"

    id: Mapped[str] = mapped_column(
        String(40), primary_key=True
    )
    request_id: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    domain: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    customer_id: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )
    request_json: Mapped[dict] = mapped_column(
        JSON, nullable=False
    )
    decision: Mapped[str] = mapped_column(
        String(30), nullable=False, index=True
    )
    decision_confidence: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    winning_policy_id: Mapped[str | None] = mapped_column(
        String(40), nullable=True, index=True
    )
    winning_policy_version: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    resolution_json: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )
    explanation_json: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )
    metrics_json: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )
    warnings_json: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )
    correlation_id: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )
    created_by: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    evaluated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    def __repr__(self) -> str:
        return (
            f"<Evaluation id={self.id} decision={self.decision}>"
        )
