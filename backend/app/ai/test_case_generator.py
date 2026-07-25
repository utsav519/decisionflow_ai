from __future__ import annotations

from app.ai.prompts.test_case_generation import SYSTEM_PROMPT
from app.ai.providers.base import LLMProvider
from app.ai.schemas.test_case import TestCaseGenerationResult


class AITestCaseGenerator:
    """
    AI service responsible for generating policy test cases.
    """

    def __init__(self, provider: LLMProvider):
        self._provider = provider

    async def generate(
        self,
        policy_definition: str,
    ) -> TestCaseGenerationResult:
        """
        Generate deterministic structured test cases for a policy.
        """

        user_prompt = f"""
Policy Definition:
{policy_definition}
""".strip()

        return await self._provider.generate_structured(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=TestCaseGenerationResult,
        )

# from __future__ import annotations

# from app.ai.providers.base import LLMProvider
# from app.ai.schemas.test_case import TestCaseGenerationResult

# from app.ai.prompts.test_case_generation import SYSTEM_PROMPT


# class AITestCaseGenerator:
#     """
#     AI service responsible for generating policy test cases.
#     """

#     def __init__(self, provider: LLMProvider):
#         self._provider = provider

#     async def generate(
#         self,
#         policy_definition: str,
#     ) -> TestCaseGenerationResult:
#         """
#         Generate deterministic structured test cases for a policy.
#         """

#         prompt = f"""
# {SYSTEM_PROMPT}

# Policy Definition:
# {policy_definition}
# """.strip()

#         return await self._provider.generate_structured(
#             system_prompt=SYSTEM_PROMPT,
#             user_prompt=policy_definition,
#             response_model=TestCaseGenerationResult,
#         )