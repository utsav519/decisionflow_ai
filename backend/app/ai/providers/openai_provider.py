from __future__ import annotations

import json

from openai import OpenAI
from pydantic import ValidationError

from app.ai.exceptions import (
    AIOutputInvalidError,
    AIProviderUnavailableError,
    AIResponseParsingError,
)
from app.ai.providers.base import LLMProvider, T


class OpenAIProvider(LLMProvider):
    def __init__(self, settings):
        self._settings = settings

        if not settings.OPENAI_API_KEY:
            raise AIProviderUnavailableError(
                message="OPENAI_API_KEY is not configured."
            )

        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def model_name(self) -> str:
        return self._settings.OPENAI_MODEL

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
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=(
                    max_output_tokens
                    or self._settings.LLM_MAX_OUTPUT_TOKENS
                ),
            )

            return response.choices[0].message.content or ""

        except Exception as ex:
            raise AIProviderUnavailableError(
                message=f"OpenAI request failed: {ex}"
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
            return response_model.model_validate(json.loads(text))

        except json.JSONDecodeError as ex:
            raise AIResponseParsingError(
                message="OpenAI returned invalid JSON."
            ) from ex

        except ValidationError as ex:
            raise AIOutputInvalidError(
                message="OpenAI response does not match expected schema."
            ) from ex