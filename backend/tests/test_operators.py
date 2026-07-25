"""
Operator tests — Spec §41 requirements.

Each operator must be tested with 4 cases:
  Match, No Match, Invalid Type, Edge/Boundary.
"""

import pytest

from app.engine.operators import get_operator, get_supported_operators
from app.engine.exceptions import UnsupportedOperatorError, OperatorTypeError


# ────────────────────────────────────────
# equals
# ────────────────────────────────────────


class TestEquals:
    def test_match(self):
        op = get_operator("equals")
        assert op(42, 42) is True
        assert op("hello", "hello") is True

    def test_no_match(self):
        op = get_operator("equals")
        assert op(42, 99) is False
        assert op("hello", "world") is False

    def test_type_coercion(self):
        """equals does not coerce types — 42 != '42'."""
        op = get_operator("equals")
        assert op(42, "42") is False

    def test_edge_none(self):
        op = get_operator("equals")
        assert op(None, None) is True
        assert op(None, 0) is False


# ────────────────────────────────────────
# not_equals
# ────────────────────────────────────────


class TestNotEquals:
    def test_match(self):
        op = get_operator("not_equals")
        assert op(42, 99) is True

    def test_no_match(self):
        op = get_operator("not_equals")
        assert op(42, 42) is False

    def test_type_coercion(self):
        op = get_operator("not_equals")
        assert op(42, "42") is True

    def test_edge_none(self):
        op = get_operator("not_equals")
        assert op(None, None) is False
        assert op(None, 0) is True


# ────────────────────────────────────────
# greater_than
# ────────────────────────────────────────


class TestGreaterThan:
    def test_match(self):
        op = get_operator("greater_than")
        assert op(100, 50) is True

    def test_no_match(self):
        op = get_operator("greater_than")
        assert op(50, 100) is False

    def test_invalid_type(self):
        op = get_operator("greater_than")
        with pytest.raises(OperatorTypeError):
            op("abc", 50)

    def test_boundary_equal(self):
        op = get_operator("greater_than")
        assert op(50, 50) is False


# ────────────────────────────────────────
# greater_than_or_equal
# ────────────────────────────────────────


class TestGreaterThanOrEqual:
    def test_match(self):
        op = get_operator("greater_than_or_equal")
        assert op(100, 50) is True

    def test_no_match(self):
        op = get_operator("greater_than_or_equal")
        assert op(49, 50) is False

    def test_invalid_type(self):
        op = get_operator("greater_than_or_equal")
        with pytest.raises(OperatorTypeError):
            op("abc", 50)

    def test_boundary_equal(self):
        op = get_operator("greater_than_or_equal")
        assert op(50, 50) is True


# ────────────────────────────────────────
# less_than
# ────────────────────────────────────────


class TestLessThan:
    def test_match(self):
        op = get_operator("less_than")
        assert op(10, 50) is True

    def test_no_match(self):
        op = get_operator("less_than")
        assert op(100, 50) is False

    def test_invalid_type(self):
        op = get_operator("less_than")
        with pytest.raises(OperatorTypeError):
            op("abc", 50)

    def test_boundary_equal(self):
        op = get_operator("less_than")
        assert op(50, 50) is False


# ────────────────────────────────────────
# less_than_or_equal
# ────────────────────────────────────────


class TestLessThanOrEqual:
    def test_match(self):
        op = get_operator("less_than_or_equal")
        assert op(10, 50) is True

    def test_no_match(self):
        op = get_operator("less_than_or_equal")
        assert op(100, 50) is False

    def test_invalid_type(self):
        op = get_operator("less_than_or_equal")
        with pytest.raises(OperatorTypeError):
            op("abc", 50)

    def test_boundary_equal(self):
        op = get_operator("less_than_or_equal")
        assert op(50, 50) is True


# ────────────────────────────────────────
# contains
# ────────────────────────────────────────


class TestContains:
    def test_match_string(self):
        op = get_operator("contains")
        assert op("hello world", "world") is True

    def test_match_list(self):
        op = get_operator("contains")
        assert op(["a", "b", "c"], "b") is True

    def test_no_match(self):
        op = get_operator("contains")
        assert op("hello", "xyz") is False

    def test_invalid_type(self):
        op = get_operator("contains")
        with pytest.raises(OperatorTypeError):
            op(42, "value")


# ────────────────────────────────────────
# in
# ────────────────────────────────────────


class TestIn:
    def test_match(self):
        op = get_operator("in")
        assert op("premium", ["basic", "premium", "enterprise"]) is True

    def test_no_match(self):
        op = get_operator("in")
        assert op("vip", ["basic", "premium"]) is False

    def test_invalid_type(self):
        op = get_operator("in")
        with pytest.raises(OperatorTypeError):
            op("value", "not_a_list")

    def test_edge_empty_list(self):
        op = get_operator("in")
        assert op("x", []) is False


# ────────────────────────────────────────
# not_in
# ────────────────────────────────────────


class TestNotIn:
    def test_match(self):
        op = get_operator("not_in")
        assert op("vip", ["basic", "premium"]) is True

    def test_no_match(self):
        op = get_operator("not_in")
        assert op("premium", ["basic", "premium"]) is False

    def test_invalid_type(self):
        op = get_operator("not_in")
        with pytest.raises(OperatorTypeError):
            op("value", "not_a_list")

    def test_edge_empty_list(self):
        op = get_operator("not_in")
        assert op("x", []) is True


# ────────────────────────────────────────
# is_empty
# ────────────────────────────────────────


class TestIsEmpty:
    def test_match_none(self):
        op = get_operator("is_empty")
        assert op(None, None) is True

    def test_match_blank_string(self):
        op = get_operator("is_empty")
        assert op("", None) is True
        assert op("   ", None) is True

    def test_match_empty_list(self):
        op = get_operator("is_empty")
        assert op([], None) is True

    def test_no_match(self):
        op = get_operator("is_empty")
        assert op("hello", None) is False
        assert op([1], None) is False


# ────────────────────────────────────────
# is_not_empty
# ────────────────────────────────────────


class TestIsNotEmpty:
    def test_match(self):
        op = get_operator("is_not_empty")
        assert op("hello", None) is True
        assert op([1, 2], None) is True

    def test_no_match_none(self):
        op = get_operator("is_not_empty")
        assert op(None, None) is False

    def test_no_match_blank(self):
        op = get_operator("is_not_empty")
        assert op("", None) is False

    def test_no_match_empty_list(self):
        op = get_operator("is_not_empty")
        assert op([], None) is False


# ────────────────────────────────────────
# Registry tests
# ────────────────────────────────────────


class TestRegistry:
    def test_unsupported_operator(self):
        with pytest.raises(UnsupportedOperatorError):
            get_operator("does_not_exist")

    def test_get_supported_operators(self):
        ops = get_supported_operators()
        ids = [o["id"] for o in ops]
        assert "equals" in ids
        assert "greater_than" in ids
        assert len(ids) == 11
