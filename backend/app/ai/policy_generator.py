# from __future__ import annotations

# from app.ai.providers.base import LLMProvider
# from app.ai.schemas.policy_generation import (
#     AIPolicyGenerationInput,
#     AIPolicyGenerationResult,
# )


# class PolicyGenerator:
#     """
#     Service responsible for generating structured policies from
#     natural language descriptions.
#     """

#     def __init__(self, provider: LLMProvider):
#         self._provider = provider

#     def generate(
#         self,
#         request: AIPolicyGenerationInput,
#     ) -> AIPolicyGenerationResult:
#         """
#         Generate a policy using the configured AI provider.
#         """

#         prompt = self._build_prompt(request)

#         return self._provider.generate_structured(
#             prompt=prompt,
#             response_model=AIPolicyGenerationResult,
#         )

#     def _build_prompt(
#         self,
#         request: AIPolicyGenerationInput,
#     ) -> str:
#         return (
#             "Generate a structured policy from the following description.\n\n"
#             f"Domain: {request.domain}\n"
#             f"Policy:\n{request.policy_text}"
#         )

from __future__ import annotations

from app.ai.providers.base import LLMProvider
from app.ai.schemas.policy_generation import (
    AIPolicyGenerationInput,
    AIPolicyGenerationResult,
)
from app.ai.prompts.policy_generation import SYSTEM_PROMPT

class PolicyGenerator:
    def __init__(self, provider: LLMProvider):
        self._provider = provider

    async def generate(
        self,
        request: AIPolicyGenerationInput,
    ) -> AIPolicyGenerationResult:

        user_prompt = self._build_prompt(request)

        return await self._provider.generate_structured(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=AIPolicyGenerationResult,
        )

    def _build_prompt(
        self,
        request: AIPolicyGenerationInput,
    ) -> str:
        return (
            "Generate a structured policy from the following description.\n\n"
            f"Domain: {request.domain}\n"
            f"Policy:\n{request.policy_text}"
        )

# Stable integration-facing alias.
AIPolicyGenerator = PolicyGenerator