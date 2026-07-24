"""
Policy repository — data access layer for policies table.

All DB interactions go through here. No business logic.

Spec reference: §28 Repository Layer
"""

from __future__ import annotations

import json
import logging
from typing import Any

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.core.ids import new_policy_id
from app.models.policy import Policy

logger = logging.getLogger(__name__)


class PolicyRepository:
    """CRUD operations on the policies table."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: dict[str, Any]) -> Policy:
        """Insert a new policy row."""
        policy = Policy(
            id=new_policy_id(),
            name=data["name"],
            description=data.get("description"),
            domain=data["domain"],
            status="DRAFT",
            priority=data["priority"],
            decision=data["decision"],
            conditions_json=data["conditions"],
            reason=data.get("reason"),
            source=data.get("source", "MANUAL"),
            current_version=1,
            ai_metadata_json=data.get("ai_metadata"),
            created_by=data.get("created_by"),
        )
        self.db.add(policy)
        self.db.flush()
        return policy

    def get_by_id(self, policy_id: str) -> Policy | None:
        """Fetch a single policy by its ID."""
        return self.db.query(Policy).filter(Policy.id == policy_id).first()

    def get_by_name(self, name: str) -> Policy | None:
        """Fetch a policy by its unique name."""
        return self.db.query(Policy).filter(Policy.name == name).first()

    def list_policies(
        self,
        page: int = 1,
        page_size: int = 20,
        status: str | None = None,
        decision: str | None = None,
        source: str | None = None,
        domain: str | None = None,
        search: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[Policy], int]:
        """Return a paginated, filtered list of policies.

        Returns:
            Tuple of (policies_for_page, total_count).
        """
        query = self.db.query(Policy)

        # Filters
        if status:
            query = query.filter(Policy.status == status)
        if decision:
            query = query.filter(Policy.decision == decision)
        if source:
            query = query.filter(Policy.source == source)
        if domain:
            query = query.filter(Policy.domain == domain)
        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Policy.name.ilike(pattern),
                    Policy.description.ilike(pattern),
                )
            )

        total = query.count()

        # Sorting
        allowed_sort_fields = {
            "created_at": Policy.created_at,
            "updated_at": Policy.updated_at,
            "priority": Policy.priority,
            "name": Policy.name,
            "status": Policy.status,
        }
        sort_col = allowed_sort_fields.get(sort_by, Policy.created_at)
        if sort_order.lower() == "asc":
            query = query.order_by(sort_col.asc())
        else:
            query = query.order_by(sort_col.desc())

        # Pagination
        offset = (page - 1) * page_size
        policies = query.offset(offset).limit(page_size).all()

        return policies, total

    def get_active_by_domain(self, domain: str) -> list[Policy]:
        """Fetch all ACTIVE policies for a domain, ordered by priority desc."""
        return (
            self.db.query(Policy)
            .filter(Policy.status == "ACTIVE", Policy.domain == domain)
            .order_by(Policy.priority.desc())
            .all()
        )

    def update(self, policy: Policy, data: dict[str, Any]) -> Policy:
        """Update mutable fields on a DRAFT policy."""
        for field in ("name", "description", "priority", "decision", "reason"):
            if field in data and data[field] is not None:
                setattr(policy, field, data[field])
        if "conditions" in data and data["conditions"] is not None:
            policy.conditions_json = data["conditions"]
        self.db.flush()
        return policy

    def delete(self, policy: Policy) -> None:
        """Hard-delete a policy (spec says archive or delete)."""
        self.db.delete(policy)
        self.db.flush()

    def count_by_status(self) -> dict[str, int]:
        """Return counts grouped by status for analytics."""
        rows = (
            self.db.query(Policy.status, func.count(Policy.id))
            .group_by(Policy.status)
            .all()
        )
        return {status: count for status, count in rows}
