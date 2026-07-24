from __future__ import annotations

from typing import Any, Type, TypeVar

from pydantic import BaseModel

from app.ai.schemas.explanation import ExplanationResult
from app.ai.schemas.provider import ProviderMetadata

from app.ai.exceptions import (
    AIOutputInvalidError,
    AIProviderTimeoutError,
    AIProviderUnavailableError,
)

from app.ai.providers.base import LLMProvider

from app.ai.schemas.ambiguity import (
    AmbiguityDetectionResult,
    AmbiguityFinding,
    ClarificationQuestion,
)

from app.ai.schemas.conflict import (
    ConflictAnalysisResult,
    ConflictReason,
    ConflictingPolicy,
)

from app.ai.schemas.policy_generation import (
    AIPolicyGenerationResult,
    GeneratedPolicy,
    GeneratedConditionGroup,
    GeneratedCondition,
    AIWarning,
    AssumptionItem,
)

from app.ai.schemas.test_case import (
    GeneratedTestCase,
    TestCaseGenerationResult,
)

T = TypeVar("T", bound=BaseModel)


class MockProvider(LLMProvider):
    """
    Deterministic mock implementation of LLMProvider.

    Used for:
    - Development
    - Offline demos
    - Unit testing
    """

    def __init__(
        self,
        settings: Any,
        *,
        simulate_timeout: bool = False,
        simulate_failure: bool = False,
    ):
        self._settings = settings
        self._simulate_timeout = simulate_timeout
        self._simulate_failure = simulate_failure

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def model_name(self) -> str:
        return "mock-v1"

    def _check_simulation(self) -> None:
        """
        Simulate provider failures for testing.
        """
        if self._simulate_failure:
            raise AIProviderUnavailableError(
                "Mock provider unavailable."
            )

        if self._simulate_timeout:
            raise AIProviderTimeoutError(
                "Mock provider timed out."
            )

    async def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: Type[T],
        temperature: float | None = None,
        max_output_tokens: int | None = None,
        timeout_seconds: int | None = None,
    ) -> T:
        """
        Return a deterministic structured response.
        """
        self._check_simulation()

        if response_model is ExplanationResult:
            return self._build_explanation_result()  # type: ignore[return-value]

        if response_model is AmbiguityDetectionResult:
            return self._build_ambiguity_result()  # type: ignore[return-value]

        if response_model is ConflictAnalysisResult:
            return self._build_conflict_result()  # type: ignore[return-value]

        if response_model is AIPolicyGenerationResult:
            return self._build_policy_result()  # type: ignore[return-value]

        if response_model is TestCaseGenerationResult:
            return self._build_test_case_result()  # type: ignore[return-value]

        raise AIOutputInvalidError(
            f"No mock response registered for {response_model.__name__}."
        )

    async def generate_text(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
        timeout_seconds: int | None = None,
    ) -> str:
        """
        Return a deterministic text response.
        """
        self._check_simulation()

        return "MockProvider deterministic response."

    def _provider_metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            provider=self.provider_name,
            model=self.model_name,
            processing_time_ms=5,
            fallback_used=False,
            retry_count=0,
            request_tokens=50,
            response_tokens=100,
            estimated_cost=0.0,
        )

    def _build_explanation_result(self) -> ExplanationResult:
        return ExplanationResult(
            summary="Loan approved because the applicant satisfies all policy conditions.",
            key_factors=[
                "Credit score exceeds minimum threshold.",
                "Fraud risk is acceptable.",
                "Income verification succeeded.",
            ],
            winning_policy_reason="Highest priority matching policy was selected.",
            competing_policy_note=None,
            generated_by="AI",
            fallback_used=False,
            provider_metadata=self._provider_metadata(),
        )

    def _build_ambiguity_result(self) -> AmbiguityDetectionResult:
        return AmbiguityDetectionResult(
            has_ambiguity=True,
            findings=[
                AmbiguityFinding(
                    field="credit_score",
                    severity="HIGH",
                    explanation="The policy does not specify whether the minimum credit score is inclusive.",
                    clarification=ClarificationQuestion(
                        question="Should applicants with a credit score of exactly 750 be approved?",
                        reason="Boundary condition is not clearly defined.",
                    ),
                ),
                AmbiguityFinding(
                    field="fraud_risk_score",
                    severity="MEDIUM",
                    explanation="Maximum fraud risk threshold is not mentioned.",
                    clarification=ClarificationQuestion(
                        question="What is the maximum acceptable fraud risk score?",
                        reason="Approval criteria are incomplete.",
                    ),
                ),
            ],
            provider_metadata=self._provider_metadata(),
        )

    def _build_conflict_result(self) -> ConflictAnalysisResult:
        return ConflictAnalysisResult(
            has_conflict=True,
            conflicting_policies=[
                ConflictingPolicy(
                    policy_id="P001",
                    policy_name="Reject High Risk",
                    priority=100,
                    decision="REJECT",
                ),
                ConflictingPolicy(
                    policy_id="P002",
                    policy_name="Approve Premium Customer",
                    priority=50,
                    decision="APPROVE",
                ),
            ],
            reasons=[
                ConflictReason(
                    description="Both policies match the same applicant.",
                    severity="HIGH",
                ),
            ],
            recommended_winner="P001",
            explanation="The higher priority policy wins according to the conflict resolution strategy.",
            provider_metadata=self._provider_metadata(),
        )

    def _build_policy_result(self) -> AIPolicyGenerationResult:
        return AIPolicyGenerationResult(
            generated_policy=GeneratedPolicy(
                policy_name="Approve Premium Customer",
                priority=100,
                decision="APPROVE",
                condition_group=GeneratedConditionGroup(
                    logical_operator="AND",
                    conditions=[
                        GeneratedCondition(
                            field="credit_score",
                            operator=">=",
                            value=750,
                        ),
                        GeneratedCondition(
                            field="fraud_risk_score",
                            operator="<=",
                            value=20,
                        ),
                        GeneratedCondition(
                            field="income_verified",
                            operator="==",
                            value=True,
                        ),
                    ],
                ),
            ),
            ai_confidence=0.96,
            validation_status="VALID",
            warnings=[
                AIWarning(
                    message="Policy generated successfully."
                )
            ],
            ambiguities=[],
            assumptions=[
                AssumptionItem(
                    description="Income verification data is available."
                )
            ],
            suggested_test_cases=[],
            provider_metadata=self._provider_metadata(),
        )

    def _build_test_case_result(self) -> TestCaseGenerationResult:
        return TestCaseGenerationResult(
            generated_test_cases=[
                GeneratedTestCase(
                    name="Eligible Customer",
                    category="POSITIVE",
                    input={
                        "age": 25,
                        "country": "India",
                        "income": 60000,
                    },
                    expected_match=True,
                    expected_decision="APPROVED",
                    rationale="Applicant satisfies all policy conditions.",
                ),
                GeneratedTestCase(
                    name="Underage Applicant",
                    category="NEGATIVE",
                    input={
                        "age": 16,
                        "country": "India",
                        "income": 60000,
                    },
                    expected_match=False,
                    expected_decision="REJECTED",
                    rationale="Applicant does not satisfy the minimum age requirement.",
                ),
                GeneratedTestCase(
                    name="Boundary Age",
                    category="BOUNDARY",
                    input={
                        "age": 18,
                        "country": "India",
                        "income": 60000,
                    },
                    expected_match=True,
                    expected_decision="APPROVED",
                    rationale="Applicant is exactly at the minimum allowed age.",
                ),
            ],
            provider_metadata=self._provider_metadata(),
        )