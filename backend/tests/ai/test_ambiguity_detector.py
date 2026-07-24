import pytest

from app.ai.ambiguity_detector import AmbiguityDetector
from app.ai.providers.mock_provider import MockProvider
from app.ai.schemas.ambiguity import AmbiguityDetectionResult


@pytest.mark.asyncio
async def test_detect_ambiguity():
    detector = AmbiguityDetector(
        MockProvider(settings=None)
    )

    result = await detector.analyze(
        "Approve users with good credit."
    )

    assert isinstance(result, AmbiguityDetectionResult)
    assert result.has_ambiguity is True