from app.ai.fallback import build_fallback_explanation


def test_winning_policy_explanation():
    result = build_fallback_explanation(
        {
            "decision": "APPROVE",
            "winning_policy": {
                "name": "Premium Upgrade"
            },
            "matched_policies": [{}],
        }
    )

    assert result.generated_by == "DETERMINISTIC_FALLBACK"
    assert result.fallback_used is True
    assert "Premium Upgrade" in result.summary


def test_no_matching_policy():
    result = build_fallback_explanation(
        {
            "decision": "MANUAL_REVIEW",
        }
    )

    assert "manual review" in result.summary.lower()


def test_missing_fields():
    result = build_fallback_explanation(
        {
            "missing_fields": [
                "credit_score",
                "income",
            ]
        }
    )

    assert "credit_score" in result.summary
    assert "income" in result.summary


def test_multiple_matched_policies():
    result = build_fallback_explanation(
        {
            "decision": "REJECT",
            "winning_policy": {
                "name": "Fraud Policy"
            },
            "matched_policies": [{}, {}],
        }
    )

    assert result.competing_policy_note is not None