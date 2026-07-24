"""
Prefixed identifier generation.

All entity IDs use readable prefixes (pol_, ver_, eval_, etc.)
backed by UUID4 for uniqueness.

Spec reference: §12 Identifier Generation
"""

from uuid import uuid4


def new_id(prefix: str) -> str:
    """Generate a prefixed unique identifier.

    Args:
        prefix: Short entity prefix (e.g. 'pol', 'ver', 'eval').

    Returns:
        String like 'pol_a1b2c3d4e5f6...'
    """
    return f"{prefix}_{uuid4().hex}"


# Convenience functions for common entity types
def new_policy_id() -> str:
    return new_id("pol")


def new_version_id() -> str:
    return new_id("ver")


def new_evaluation_id() -> str:
    return new_id("eval")


def new_rule_result_id() -> str:
    return new_id("rr")


def new_audit_id() -> str:
    return new_id("aud")


def new_correlation_id() -> str:
    return new_id("cor")
