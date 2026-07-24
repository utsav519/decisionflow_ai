from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMProvider(ABC):
    """
    Abstract base class for all Large Language Model providers.

    Every provider (OpenAI, Gemini, Anthropic, Groq, Mock)
    must implement this interface.
    """

    @abstractmethod
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
        """
        Generate structured output that conforms to the supplied
        Pydantic response model.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_text(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0,
        max_output_tokens: int | None = None,
        timeout_seconds: int | None = None,
    ) -> str:
        """
        Generate plain text output.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Returns the provider name.
        Example:
            openai
            gemini
            groq
            mock
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Returns the configured model name.
        """
        raise NotImplementedError