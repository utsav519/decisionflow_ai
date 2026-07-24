from app.ai.confidence import AIPolicyConfidenceCalculator


class DummyAmbiguity:
    def __init__(self, severity: str):
        self.severity = severity


class DummyWarning:
    def __init__(self, code: str):
        self.code = code


def test_clean_policy_receives_high_score():
    calculator = AIPolicyConfidenceCalculator()

    score = calculator.calculate(
        policy_text="Approve customers with credit score >= 750",
        generated_policy={"name": "Policy"},
        ambiguities=[],
        assumptions=[],
        warnings=[],
        local_validation_errors=[],
    )

    assert score == 100


def test_blocking_ambiguity_reduces_score():
    calculator = AIPolicyConfidenceCalculator()

    score = calculator.calculate(
        policy_text="Approve loyal customers",
        generated_policy={"name": "Policy"},
        ambiguities=[DummyAmbiguity("BLOCKING")],
        assumptions=[],
        warnings=[],
        local_validation_errors=[],
    )

    assert score == 75


def test_unsupported_field_reduces_score():
    calculator = AIPolicyConfidenceCalculator()

    score = calculator.calculate(
        policy_text="...",
        generated_policy={"name": "Policy"},
        ambiguities=[],
        assumptions=[],
        warnings=[],
        local_validation_errors=[
            {"code": "UNSUPPORTED_FIELD"}
        ],
    )

    assert score == 70


def test_assumptions_reduce_score():
    calculator = AIPolicyConfidenceCalculator()

    score = calculator.calculate(
        policy_text="...",
        generated_policy={"name": "Policy"},
        ambiguities=[],
        assumptions=[
            "A1",
            "A2",
            "A3",
        ],
        warnings=[],
        local_validation_errors=[],
    )

    assert score == 91


def test_provider_fallback_reduces_score():
    calculator = AIPolicyConfidenceCalculator()

    score = calculator.calculate(
        policy_text="...",
        generated_policy={"name": "Policy"},
        ambiguities=[],
        assumptions=[],
        warnings=[],
        local_validation_errors=[],
        provider_fallback=True,
    )

    assert score == 90


def test_score_is_clamped_between_zero_and_hundred():
    calculator = AIPolicyConfidenceCalculator()

    score = calculator.calculate(
        policy_text="...",
        generated_policy=None,
        ambiguities=[DummyAmbiguity("BLOCKING")] * 10,
        assumptions=["A"] * 20,
        warnings=[],
        local_validation_errors=[
            {"code": "UNSUPPORTED_FIELD"}
        ] * 10,
        provider_fallback=True,
    )

    assert 0 <= score <= 100


def test_same_input_produces_same_score():
    calculator = AIPolicyConfidenceCalculator()

    kwargs = dict(
        policy_text="...",
        generated_policy={"name": "Policy"},
        ambiguities=[DummyAmbiguity("WARNING")],
        assumptions=["A1"],
        warnings=[DummyWarning("INFERRED_PRIORITY")],
        local_validation_errors=[],
    )

    score1 = calculator.calculate(**kwargs)
    score2 = calculator.calculate(**kwargs)

    assert score1 == score2