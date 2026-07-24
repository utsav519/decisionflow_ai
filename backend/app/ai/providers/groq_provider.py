from __future__ import annotations

import json

from groq import Groq
from pydantic import ValidationError

# from app.ai.exceptions import AIProviderError
from app.ai.exceptions import (
    AIProviderUnavailableError,
    AIOutputInvalidError,
    AIResponseParsingError,
)
from app.ai.providers.base import LLMProvider, T


class GroqProvider(LLMProvider):
    def __init__(self, settings):
        self._settings = settings

        if not settings.GROQ_API_KEY:
            raise AIProviderUnavailableError(
                message="GROQ_API_KEY is not configured."
            )

        self._client = Groq(api_key=settings.GROQ_API_KEY)

    @property
    def provider_name(self) -> str:
        return "groq"

    @property
    def model_name(self) -> str:
        return self._settings.LLM_MODEL

    async def generate_text(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0,
        max_output_tokens: int | None = None,
        timeout_seconds: int | None = None,
    ) -> str:

        try:
            response = self._client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=temperature,
                max_completion_tokens=(
                    max_output_tokens
                    or self._settings.LLM_MAX_OUTPUT_TOKENS
                ),
            )

            return response.choices[0].message.content or ""

        except Exception as ex:
            raise AIProviderUnavailableError(
                message=f"Groq request failed: {ex}"
            ) from ex

    async def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
        temperature: float = 0,
        max_output_tokens: int | None = None,
        timeout_seconds: int | None = None,
    ) -> T:

        text = await self.generate_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            timeout_seconds=timeout_seconds,
        )

        try:
            data = json.loads(text)
            return response_model.model_validate(data)

        except json.JSONDecodeError as ex:
            raise AIResponseParsingError(
                message="Groq returned invalid JSON."
            ) from ex

        except ValidationError as ex:
            raise AIOutputInvalidError(
                message="Groq response does not match expected schema."
            ) from ex