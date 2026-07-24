from __future__ import annotations

import json

from google import genai
from pydantic import ValidationError

from app.ai.exceptions import (
    AIOutputInvalidError,
    AIProviderUnavailableError,
    AIResponseParsingError,
)
from app.ai.providers.base import LLMProvider, T


class GeminiProvider(LLMProvider):
    def __init__(self, settings):
        self._settings = settings

        if not settings.GEMINI_API_KEY:
            raise AIProviderUnavailableError(
                message="GEMINI_API_KEY is not configured."
            )

        self._client = genai.Client(api_key=settings.GEMINI_API_KEY)

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def model_name(self) -> str:
        return self._settings.GEMINI_MODEL

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
            prompt = f"{system_prompt}\n\n{user_prompt}"

            response = self._client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )

            return response.text or ""

        except Exception as ex:
            raise AIProviderUnavailableError(
                message=f"Gemini request failed: {ex}"
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
                message="Gemini returned invalid JSON."
            ) from ex

        except ValidationError as ex:
            raise AIOutputInvalidError(
                message="Gemini response does not match expected schema."
            ) from ex