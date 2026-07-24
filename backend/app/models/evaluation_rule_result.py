"""
Evaluation rule result ORM model.

Stores the per-policy evaluation trace for each decision evaluation.

Spec reference: §11.4 Evaluation rule result model
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EvaluationRuleResult(Base):
    """Stores the evaluation trace for a single policy."""

    __tablename__ = "evaluation_rule_results"

    id: Mapped[str] = mapped_column(
        String(40), primary_key=True
    )
    evaluation_id: Mapped[str] = mapped_column(
        String(40), nullable=False, index=True
    )
    policy_id: Mapped[str] = mapped_column(
        String(40), nullable=False, index=True
    )
    policy_version: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    policy_name: Mapped[str] = mapped_column(
        String(120), nullable=False
    )
    priority: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    decision: Mapped[str] = mapped_column(
        String(30), nullable=False
    )
    result_status: Mapped[str] = mapped_column(
        String(40), nullable=False
    )
    matched: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )
    condition_results_json: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )
    missing_fields_json: Mapped[list | None] = mapped_column(
        JSON, nullable=True
    )
    reason: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        default=datetime.utcnow,
    )

    def __repr__(self) -> str:
        return (
            f"<EvaluationRuleResult evaluation_id="
            f"{self.evaluation_id} policy_id={self.policy_id} "
            f"matched={self.matched}>"
        )
