from __future__ import annotations

import json

from anthropic import Anthropic
from pydantic import ValidationError

from app.ai.exceptions import (
    AIOutputInvalidError,
    AIProviderUnavailableError,
    AIResponseParsingError,
)
from app.ai.providers.base import LLMProvider, T


class AnthropicProvider(LLMProvider):
    def __init__(self, settings):
        self._settings = settings

        if not settings.ANTHROPIC_API_KEY:
            raise AIProviderUnavailableError(
                message="ANTHROPIC_API_KEY is not configured."
            )

        self._client = Anthropic(
            api_key=settings.ANTHROPIC_API_KEY
        )

    @property
    def provider_name(self) -> str:
        return "anthropic"

    @property
    def model_name(self) -> str:
        return self._settings.ANTHROPIC_MODEL

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
            response = self._client.messages.create(
                model=self.model_name,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
                temperature=temperature,
                max_tokens=(
                    max_output_tokens
                    or self._settings.LLM_MAX_OUTPUT_TOKENS
                ),
            )

            return response.content[0].text

        except Exception as ex:
            raise AIProviderUnavailableError(
                message=f"Anthropic request failed: {ex}"
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
                message="Anthropic returned invalid JSON."
            ) from ex

        except ValidationError as ex:
            raise AIOutputInvalidError(
                message="Anthropic response does not match expected schema."
            ) from ex