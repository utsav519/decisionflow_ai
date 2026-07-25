from __future__ import annotations

import pytest

from app.ai.providers.mock_provider import MockProvider
from app.ai.schemas.test_case import TestCaseGenerationResult
from app.ai.test_case_generator import AITestCaseGenerator


class DummySettings:
    pass


@pytest.mark.asyncio
async def test_generate_returns_test_case_result():
    provider = MockProvider(DummySettings())
    generator = AITestCaseGenerator(provider)

    result = await generator.generate(
        """
        Approve if:
        - age >= 18
        - income >= 50000
        """
    )

    assert isinstance(result, TestCaseGenerationResult)
    assert len(result.generated_test_cases) == 3

    assert result.generated_test_cases[0].name == "Eligible Customer"
    assert result.generated_test_cases[0].category == "POSITIVE"

    assert result.generated_test_cases[1].name == "Underage Applicant"
    assert result.generated_test_cases[1].category == "NEGATIVE"

    assert result.generated_test_cases[2].name == "Boundary Age"
    assert result.generated_test_cases[2].category == "BOUNDARY"


@pytest.mark.asyncio
async def test_generate_returns_provider_metadata():
    provider = MockProvider(DummySettings())
    generator = AITestCaseGenerator(provider)

    result = await generator.generate("sample policy")

    assert result.provider_metadata.provider == "mock"
    assert result.provider_metadata.model == "mock-v1"
    assert result.provider_metadata.processing_time_ms == 5


@pytest.mark.asyncio
async def test_generate_is_deterministic():
    provider = MockProvider(DummySettings())
    generator = AITestCaseGenerator(provider)

    first = await generator.generate("policy")
    second = await generator.generate("policy")

    assert first == second