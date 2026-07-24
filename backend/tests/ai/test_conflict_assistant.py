import pytest

from app.ai.conflict_assistant import ConflictAssistant
from app.ai.providers.mock_provider import MockProvider
from app.ai.schemas.conflict import ConflictAnalysisResult


@pytest.mark.asyncio
async def test_conflict_analysis():
    assistant = ConflictAssistant(
        MockProvider(settings=None)
    )

    result = await assistant.analyze(
        "Approve",
        "Reject",
    )

    assert isinstance(result, ConflictAnalysisResult)
    assert result.has_conflict is True