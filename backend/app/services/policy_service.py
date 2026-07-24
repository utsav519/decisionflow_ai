"""
Policy service — business logic for policy lifecycle.

Orchestrates repository calls, validation, versioning, and audit logging.
This is the ONLY place where status transitions are enforced.

Spec reference: §26 Policy Lifecycle, §27 Validation
"""

from __future__ import annotations

import logging
import math
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import (
    DuplicatePolicyNameError,
    InvalidPolicyStateError,
    PolicyNotFoundError,
    PolicyValidationError,
)
from app.repositories.audit_repository import AuditRepository
from app.repositories.policy_repository import PolicyRepository
from app.repositories.policy_version_repository import PolicyVersionRepository
from app.services.audit_service import AuditService
from app.services.validation_service import validate_conditions

logger = logging.getLogger(__name__)


class PolicyService:
    """Business logic for the policy lifecycle."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.policy_repo = PolicyRepository(db)
        self.version_repo = PolicyVersionRepository(db)
        self.audit_service = AuditService(db)

    # ─── CREATE ───────────────────────────────────────

    def create_policy(
        self,
        data: dict[str, Any],
        performed_by: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Create a new policy in DRAFT status.

        Args:
            data: Validated PolicyCreate fields.
            performed_by: Actor identity.
            correlation_id: Request correlation ID.

        Returns:
            Dict with the created policy data and validation metadata.
        """
        # Check duplicate name
        existing = self.policy_repo.get_by_name(data["name"])
        if existing:
            raise DuplicatePolicyNameError(data["name"])

        # Validate conditions
        validation = validate_conditions(data["conditions"], data["domain"])

        # Force DRAFT status (spec §26 — server overrides)
        data["created_by"] = performed_by

        policy = self.policy_repo.create(data)

        # Create initial version snapshot
        self.version_repo.create_snapshot(policy)

        # Audit
        result_data = self._policy_to_dict(policy)
        self.audit_service.log_policy_created(
            policy_id=policy.id,
            version=policy.current_version,
            request_data=data,
            result_data=result_data,
            performed_by=performed_by,
            correlation_id=correlation_id,
        )

        self.db.commit()

        return {
            "policy": result_data,
            "validation_status": validation.status,
            "validation_warnings": validation.warnings,
        }

    # ─── READ ─────────────────────────────────────────

    def get_policy(self, policy_id: str) -> dict[str, Any]:
        """Get a policy by ID."""
        policy = self.policy_repo.get_by_id(policy_id)
        if not policy:
            raise PolicyNotFoundError(policy_id)
        return self._policy_to_dict(policy)

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
    ) -> dict[str, Any]:
        """List policies with pagination and filters."""
        policies, total = self.policy_repo.list_policies(
            page=page,
            page_size=page_size,
            status=status,
            decision=decision,
            source=source,
            domain=domain,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return {
            "policies": [self._policy_to_list_item(p) for p in policies],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": total,
                "total_pages": max(1, math.ceil(total / page_size)),
            },
        }

    def get_active_policies(self, domain: str) -> list[dict[str, Any]]:
        """Get all active policies for a specific domain."""
        policies = self.policy_repo.get_active_by_domain(domain)
        return [self._policy_to_dict(p) for p in policies]

    # ─── UPDATE ───────────────────────────────────────

    def update_policy(
        self,
        policy_id: str,
        data: dict[str, Any],
        performed_by: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Update a DRAFT policy's mutable fields."""
        policy = self.policy_repo.get_by_id(policy_id)
        if not policy:
            raise PolicyNotFoundError(policy_id)

        if policy.status != "DRAFT":
            raise InvalidPolicyStateError(policy.status, "update")

        # Check duplicate name if name is changing
        if "name" in data and data["name"] and data["name"] != policy.name:
            existing = self.policy_repo.get_by_name(data["name"])
            if existing:
                raise DuplicatePolicyNameError(data["name"])

        # Validate new conditions if provided
        if "conditions" in data and data["conditions"] is not None:
            validation = validate_conditions(data["conditions"], policy.domain)
        else:
            validation = None

        self.policy_repo.update(policy, data)

        result_data = self._policy_to_dict(policy)
        self.audit_service.log_policy_updated(
            policy_id=policy.id,
            version=policy.current_version,
            request_data=data,
            result_data=result_data,
            performed_by=performed_by,
            correlation_id=correlation_id,
        )

        self.db.commit()

        return {
            "policy": result_data,
            "validation_status": validation.status if validation else "SKIPPED",
            "validation_warnings": validation.warnings if validation else [],
        }

    # ─── ACTIVATE ─────────────────────────────────────

    def activate_policy(
        self,
        policy_id: str,
        performed_by: str,
        correlation_id: str,
        approval_comment: str | None = None,
    ) -> dict[str, Any]:
        """Activate a DRAFT or DISABLED policy."""
        policy = self.policy_repo.get_by_id(policy_id)
        if not policy:
            raise PolicyNotFoundError(policy_id)

        allowed = ("DRAFT", "DISABLED")
        if policy.status not in allowed:
            raise InvalidPolicyStateError(policy.status, "activate")

        # Validate conditions before activation
        validation = validate_conditions(policy.conditions_json, policy.domain)
        if not validation.passed:
            raise PolicyValidationError(
                message="Policy cannot be activated: validation failed.",
                details=validation.errors,
            )

        # Bump version and status
        policy.current_version += 1
        policy.status = "ACTIVE"
        policy.approved_by = performed_by
        policy.activated_at = datetime.utcnow()
        self.db.flush()

        # Create version snapshot
        self.version_repo.create_snapshot(policy)

        self.audit_service.log_policy_activated(
            policy_id=policy.id,
            version=policy.current_version,
            performed_by=performed_by,
            correlation_id=correlation_id,
            approval_comment=approval_comment,
        )

        self.db.commit()

        return {
            "policy": self._policy_to_dict(policy),
            "validation_status": validation.status,
            "validation_warnings": validation.warnings,
        }

    # ─── DISABLE ──────────────────────────────────────

    def disable_policy(
        self,
        policy_id: str,
        performed_by: str,
        correlation_id: str,
        reason: str | None = None,
    ) -> dict[str, Any]:
        """Disable an ACTIVE policy."""
        policy = self.policy_repo.get_by_id(policy_id)
        if not policy:
            raise PolicyNotFoundError(policy_id)

        if policy.status != "ACTIVE":
            raise InvalidPolicyStateError(policy.status, "disable")

        policy.status = "DISABLED"
        policy.disabled_at = datetime.utcnow()
        self.db.flush()

        self.audit_service.log_policy_disabled(
            policy_id=policy.id,
            version=policy.current_version,
            performed_by=performed_by,
            correlation_id=correlation_id,
            reason=reason,
        )

        self.db.commit()

        return {"policy": self._policy_to_dict(policy)}

    # ─── DELETE ───────────────────────────────────────

    def delete_policy(
        self,
        policy_id: str,
        performed_by: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Delete (archive) a policy."""
        policy = self.policy_repo.get_by_id(policy_id)
        if not policy:
            raise PolicyNotFoundError(policy_id)

        policy_data = self._policy_to_dict(policy)
        self.audit_service.log_policy_deleted(
            policy_id=policy.id,
            version=policy.current_version,
            performed_by=performed_by,
            correlation_id=correlation_id,
        )

        self.policy_repo.delete(policy)
        self.db.commit()

        return {"policy": policy_data, "message": "Policy deleted successfully."}

    # ─── HELPERS ──────────────────────────────────────

    def _policy_to_dict(self, policy) -> dict[str, Any]:
        """Convert a Policy ORM object to a response dict."""
        return {
            "id": policy.id,
            "version": policy.current_version,
            "name": policy.name,
            "description": policy.description,
            "domain": policy.domain,
            "status": policy.status,
            "priority": policy.priority,
            "decision": policy.decision,
            "conditions": policy.conditions_json,
            "reason": policy.reason,
            "source": policy.source,
            "ai_metadata": policy.ai_metadata_json,
            "created_by": policy.created_by,
            "approved_by": policy.approved_by,
            "created_at": policy.created_at.isoformat() if policy.created_at else None,
            "updated_at": policy.updated_at.isoformat() if policy.updated_at else None,
            "activated_at": policy.activated_at.isoformat() if policy.activated_at else None,
            "disabled_at": policy.disabled_at.isoformat() if policy.disabled_at else None,
        }

    def _policy_to_list_item(self, policy) -> dict[str, Any]:
        """Convert a Policy ORM object to a lightweight list item."""
        return {
            "id": policy.id,
            "version": policy.current_version,
            "name": policy.name,
            "domain": policy.domain,
            "status": policy.status,
            "priority": policy.priority,
            "decision": policy.decision,
            "created_by": policy.created_by,
            "updated_at": policy.updated_at.isoformat() if policy.updated_at else None,
        }
