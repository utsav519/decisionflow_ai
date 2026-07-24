"""
Evaluator tests — Spec §42 requirements.

15 required test scenarios:
  1. Single matching condition
  2. Single non-matching condition
  3. 'all' group matches
  4. 'all' group fails
  5. 'any' group matches
  6. 'any' group fails
  7. Nested group
  8. Missing field
  9. Unsupported operator
  10. Invalid value type
  11. Multiple matching policies
  12. No policies
  13. No matching policies
  14. Performance metric present
  15. Input objects are not mutated
"""

import copy

import pytest

from app.engine.evaluator import evaluate_policies, evaluate_policy


def _make_policy(
    pid="pol_test1",
    name="Test Policy",
    version=1,
    priority=100,
    decision="APPROVE",
    conditions=None,
):
    return {
        "id": pid,
        "name": name,
        "current_version": version,
        "priority": priority,
        "decision": decision,
        "conditions_json": conditions or {"all": [{"field": "score", "operator": "greater_than", "value": 50}]},
    }


class TestEvaluator:
    """Spec §42: 15 required evaluator test scenarios."""

    # 1. Single matching condition
    def test_single_matching_condition(self):
        policy = _make_policy(conditions={"all": [{"field": "score", "operator": "equals", "value": 700}]})
        result = evaluate_policy(policy, {"score": 700})
        assert result.matched is True
        assert result.result_status == "MATCHED"
        assert len(result.condition_results) == 1
        assert result.condition_results[0].status == "MATCHED"

    # 2. Single non-matching condition
    def test_single_non_matching_condition(self):
        policy = _make_policy(conditions={"all": [{"field": "score", "operator": "equals", "value": 700}]})
        result = evaluate_policy(policy, {"score": 500})
        assert result.matched is False
        assert result.result_status == "UNMATCHED"

    # 3. 'all' group matches
    def test_all_group_matches(self):
        policy = _make_policy(conditions={
            "all": [
                {"field": "score", "operator": "greater_than", "value": 600},
                {"field": "defaults", "operator": "equals", "value": 0},
            ]
        })
        result = evaluate_policy(policy, {"score": 700, "defaults": 0})
        assert result.matched is True

    # 4. 'all' group fails
    def test_all_group_fails(self):
        policy = _make_policy(conditions={
            "all": [
                {"field": "score", "operator": "greater_than", "value": 600},
                {"field": "defaults", "operator": "equals", "value": 0},
            ]
        })
        result = evaluate_policy(policy, {"score": 700, "defaults": 3})
        assert result.matched is False

    # 5. 'any' group matches
    def test_any_group_matches(self):
        policy = _make_policy(conditions={
            "any": [
                {"field": "plan", "operator": "equals", "value": "premium"},
                {"field": "score", "operator": "greater_than", "value": 800},
            ]
        })
        result = evaluate_policy(policy, {"plan": "basic", "score": 900})
        assert result.matched is True

    # 6. 'any' group fails
    def test_any_group_fails(self):
        policy = _make_policy(conditions={
            "any": [
                {"field": "plan", "operator": "equals", "value": "premium"},
                {"field": "score", "operator": "greater_than", "value": 800},
            ]
        })
        result = evaluate_policy(policy, {"plan": "basic", "score": 500})
        assert result.matched is False

    # 7. Nested group
    def test_nested_group(self):
        policy = _make_policy(conditions={
            "all": [
                {"field": "score", "operator": "greater_than", "value": 600},
                {"any": [
                    {"field": "plan", "operator": "equals", "value": "premium"},
                    {"field": "tenure", "operator": "greater_than", "value": 24},
                ]},
            ]
        })
        result = evaluate_policy(policy, {"score": 700, "plan": "basic", "tenure": 36})
        assert result.matched is True

    # 8. Missing field
    def test_missing_field(self):
        policy = _make_policy(conditions={
            "all": [{"field": "nonexistent_field", "operator": "equals", "value": 42}]
        })
        result = evaluate_policy(policy, {"score": 700})
        assert result.matched is False
        assert "nonexistent_field" in result.missing_fields
        assert result.condition_results[0].status == "MISSING_FIELD"

    # 9. Unsupported operator
    def test_unsupported_operator(self):
        policy = _make_policy(conditions={
            "all": [{"field": "score", "operator": "regex_match", "value": ".*"}]
        })
        result = evaluate_policy(policy, {"score": 700})
        assert result.matched is False
        assert result.condition_results[0].status == "ERROR"

    # 10. Invalid value type
    def test_invalid_value_type(self):
        policy = _make_policy(conditions={
            "all": [{"field": "name", "operator": "greater_than", "value": 50}]
        })
        result = evaluate_policy(policy, {"name": "Alice"})
        assert result.matched is False
        assert result.condition_results[0].status == "INVALID_VALUE"

    # 11. Multiple matching policies
    def test_multiple_matching_policies(self):
        policies = [
            _make_policy(pid="pol_1", priority=100, conditions={"all": [{"field": "score", "operator": "greater_than", "value": 50}]}),
            _make_policy(pid="pol_2", priority=200, conditions={"all": [{"field": "score", "operator": "greater_than", "value": 50}]}),
        ]
        result = evaluate_policies(policies, {"score": 700})
        assert len(result.matched) == 2

    # 12. No policies
    def test_no_policies(self):
        result = evaluate_policies([], {"score": 700})
        assert len(result.matched) == 0
        assert len(result.unmatched) == 0
        assert len(result.skipped) == 0
        assert "No active policies" in result.warnings[0]

    # 13. No matching policies
    def test_no_matching_policies(self):
        policies = [
            _make_policy(conditions={"all": [{"field": "score", "operator": "greater_than", "value": 900}]}),
        ]
        result = evaluate_policies(policies, {"score": 500})
        assert len(result.matched) == 0
        assert len(result.unmatched) == 1

    # 14. Performance metric present
    def test_performance_metric_present(self):
        policies = [_make_policy()]
        result = evaluate_policies(policies, {"score": 700})
        assert result.evaluation_time_ms >= 0

    # 15. Input objects are not mutated
    def test_input_objects_not_mutated(self):
        data = {"score": 700, "nested": {"key": "value"}}
        data_before = copy.deepcopy(data)
        policies = [_make_policy()]
        policies_before = copy.deepcopy(policies)

        evaluate_policies(policies, data)

        assert data == data_before, "Input data was mutated!"
        assert policies == policies_before, "Input policies were mutated!"
