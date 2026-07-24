"""
Policy version repository — data access for immutable version snapshots.

Spec reference: §26 Version Snapshot Management
"""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.core.ids import new_version_id
from app.models.policy import Policy
from app.models.policy_version import PolicyVersion


class PolicyVersionRepository:
    """CRUD operations on the policy_versions table."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_snapshot(self, policy: Policy) -> PolicyVersion:
        """Create an immutable version snapshot from the current policy state."""
        snapshot = PolicyVersion(
            id=new_version_id(),
            policy_id=policy.id,
            version=policy.current_version,
            name=policy.name,
            description=policy.description,
            domain=policy.domain,
            status_snapshot=policy.status,
            priority=policy.priority,
            decision=policy.decision,
            conditions_json=policy.conditions_json,
            reason=policy.reason,
            source=policy.source,
            ai_metadata_json=policy.ai_metadata_json,
            created_by=policy.created_by,
            approved_by=policy.approved_by,
        )
        self.db.add(snapshot)
        self.db.flush()
        return snapshot

    def get_versions_for_policy(self, policy_id: str) -> list[PolicyVersion]:
        """Fetch all version snapshots for a given policy."""
        return (
            self.db.query(PolicyVersion)
            .filter(PolicyVersion.policy_id == policy_id)
            .order_by(PolicyVersion.version.desc())
            .all()
        )

    def get_latest_version(self, policy_id: str) -> PolicyVersion | None:
        """Fetch the most recent version snapshot for a policy."""
        return (
            self.db.query(PolicyVersion)
            .filter(PolicyVersion.policy_id == policy_id)
            .order_by(PolicyVersion.version.desc())
            .first()
        )
