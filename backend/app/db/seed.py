"""
Seed data — idempotent seeding of the 5 required policies.

Running this twice must NOT create duplicates.

Spec reference: §39 Seed Data
"""

from __future__ import annotations

import logging
import sys

from sqlalchemy.orm import Session

from app.core.ids import new_policy_id, new_version_id
from app.db.session import SessionLocal
from app.models.policy import Policy
from app.models.policy_version import PolicyVersion

logger = logging.getLogger(__name__)

SEED_POLICIES = [
    {
        "name": "Fraud rejection",
        "description": "Reject applications with clear fraud indicators",
        "domain": "telecom",
        "status": "ACTIVE",
        "priority": 300,
        "decision": "REJECT",
        "conditions_json": {
            "all": [
                {"field": "customer.credit_score", "operator": "less_than", "value": 300},
                {"field": "customer.payment_history_defaults", "operator": "greater_than", "value": 5},
            ]
        },
        "reason": "Extremely low credit score combined with multiple payment defaults.",
        "source": "SEEDED",
    },
    {
        "name": "Fraud manual review",
        "description": "Flag borderline fraud cases for human review",
        "domain": "telecom",
        "status": "ACTIVE",
        "priority": 250,
        "decision": "MANUAL_REVIEW",
        "conditions_json": {
            "any": [
                {"field": "customer.credit_score", "operator": "less_than", "value": 500},
                {"field": "customer.payment_history_defaults", "operator": "greater_than", "value": 2},
            ]
        },
        "reason": "Borderline credit indicators require manual assessment.",
        "source": "SEEDED",
    },
    {
        "name": "Outstanding balance rejection",
        "description": "Reject customers with significant outstanding balances",
        "domain": "telecom",
        "status": "ACTIVE",
        "priority": 220,
        "decision": "REJECT",
        "conditions_json": {
            "all": [
                {"field": "account.outstanding_balance", "operator": "greater_than", "value": 500},
                {"field": "account.status", "operator": "not_equals", "value": "current"},
            ]
        },
        "reason": "Outstanding balance exceeds threshold with non-current account.",
        "source": "SEEDED",
    },
    {
        "name": "Standard upgrade approval",
        "description": "Approve standard plan upgrades for good customers",
        "domain": "telecom",
        "status": "ACTIVE",
        "priority": 100,
        "decision": "APPROVE",
        "conditions_json": {
            "all": [
                {"field": "customer.credit_score", "operator": "greater_than_or_equal", "value": 650},
                {"field": "customer.payment_history_defaults", "operator": "equals", "value": 0},
                {"field": "customer.tenure_months", "operator": "greater_than_or_equal", "value": 12},
            ]
        },
        "reason": "Customer meets all standard approval criteria.",
        "source": "SEEDED",
    },
    {
        "name": "Premium override approval",
        "description": "Approve premium upgrades for high-value customers",
        "domain": "telecom",
        "status": "ACTIVE",
        "priority": 120,
        "decision": "APPROVE",
        "conditions_json": {
            "all": [
                {"field": "customer.credit_score", "operator": "greater_than_or_equal", "value": 750},
                {"field": "customer.plan_type", "operator": "in", "value": ["premium", "enterprise"]},
            ]
        },
        "reason": "High credit score with existing premium/enterprise plan.",
        "source": "SEEDED",
    },
]


def seed_policies(db: Session) -> int:
    """Insert seed policies idempotently. Returns number of new policies created."""
    created = 0
    for seed in SEED_POLICIES:
        existing = db.query(Policy).filter(Policy.name == seed["name"]).first()
        if existing:
            logger.info("Seed policy '%s' already exists — skipping.", seed["name"])
            continue

        policy = Policy(
            id=new_policy_id(),
            name=seed["name"],
            description=seed["description"],
            domain=seed["domain"],
            status=seed["status"],
            priority=seed["priority"],
            decision=seed["decision"],
            conditions_json=seed["conditions_json"],
            reason=seed["reason"],
            source=seed["source"],
            current_version=1,
            created_by="system_seed",
        )
        db.add(policy)
        db.flush()

        # Create version snapshot
        version = PolicyVersion(
            id=new_version_id(),
            policy_id=policy.id,
            version=1,
            name=policy.name,
            description=policy.description,
            domain=policy.domain,
            status_snapshot=policy.status,
            priority=policy.priority,
            decision=policy.decision,
            conditions_json=policy.conditions_json,
            reason=policy.reason,
            source=policy.source,
            created_by="system_seed",
        )
        db.add(version)

        created += 1
        logger.info("Seeded policy '%s' (priority=%d, decision=%s)", seed["name"], seed["priority"], seed["decision"])

    db.commit()
    logger.info("Seed complete: %d new policies, %d already existed.", created, len(SEED_POLICIES) - created)
    return created


if __name__ == "__main__":
    from app.core.logging import setup_logging
    setup_logging("INFO")
    db = SessionLocal()
    try:
        count = seed_policies(db)
        print(f"Seeded {count} policies.")
    finally:
        db.close()
