"""
Domain catalogue registry.

Provides the schema fields specific to each supported business domain.

Spec reference: §20 Supported Operators (domain context)
"""

from typing import Any


class DomainCatalogue:
    """Registry of known fields for validation."""

    DOMAINS = {
        "telecom": {
            "customer.credit_score": "int",
            "customer.tenure_months": "int",
            "customer.payment_history_defaults": "int",
            "customer.plan_type": "str",
            "usage.average_monthly_data_gb": "float",
            "usage.international_calls_count": "int",
            "account.status": "str",
            "account.outstanding_balance": "float",
        },
        "finance": {
            "customer.credit_score": "int",
            "customer.annual_income": "float",
            "customer.employment_status": "str",
            "loan.amount": "float",
            "loan.term_months": "int",
            "account.status": "str",
        }
    }

    @classmethod
    def get_fields_for_domain(cls, domain: str) -> dict[str, str]:
        """Return the schema fields for a specific domain."""
        return cls.DOMAINS.get(domain.lower(), {})

    @classmethod
    def get_all_fields(cls) -> list[dict[str, Any]]:
        """Return all fields flattened for the config API."""
        result = []
        for domain, fields in cls.DOMAINS.items():
            for field, type_str in fields.items():
                result.append({
                    "domain": domain,
                    "field": field,
                    "type": type_str,
                })
        return result
