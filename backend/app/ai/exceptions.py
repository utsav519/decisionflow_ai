from __future__ import annotations

from typing import Any


class AIError(Exception):
    """
    Base exception for all AI module errors.
    """

    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

        super().__init__(message)

    def to_dict(self) -> dict[str, Any]:
        """
        Safe representation for API responses.
        Never include provider SDK exceptions or secrets.
        """
        return {
            "code": self.code,
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details,
        }


class AIProviderUnavailableError(AIError):
    def __init__(
        self,
        message: str = "AI provider is unavailable.",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="AI_PROVIDER_UNAVAILABLE",
            message=message,
            status_code=503,
            details=details,
        )


class AIProviderTimeoutError(AIError):
    def __init__(
        self,
        message: str = "AI provider request timed out.",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="AI_PROVIDER_TIMEOUT",
            message=message,
            status_code=504,
            details=details,
        )


class AIProviderAuthenticationError(AIError):
    def __init__(
        self,
        message: str = "AI provider authentication failed.",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="AI_PROVIDER_AUTHENTICATION_FAILED",
            message=message,
            status_code=401,
            details=details,
        )


class AIOutputInvalidError(AIError):
    def __init__(
        self,
        message: str = "Provider returned invalid structured output.",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="AI_OUTPUT_INVALID",
            message=message,
            status_code=422,
            details=details,
        )


class AIResponseParsingError(AIError):
    def __init__(
        self,
        message: str = "Failed to parse provider response.",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="AI_RESPONSE_PARSING_ERROR",
            message=message,
            status_code=422,
            details=details,
        )


class AIUnsupportedProviderError(AIError):
    def __init__(
        self,
        provider: str,
    ) -> None:
        super().__init__(
            code="UNSUPPORTED_LLM_PROVIDER",
            message=f"Unsupported LLM provider: '{provider}'.",
            status_code=400,
            details={"provider": provider},
        )


class AIPromptInputError(AIError):
    def __init__(
        self,
        message: str = "Invalid prompt input.",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="AI_PROMPT_INPUT_ERROR",
            message=message,
            status_code=400,
            details=details,
        )


class AIContentSafetyError(AIError):
    def __init__(
        self,
        message: str = "Request blocked by AI content safety.",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="AI_CONTENT_SAFETY",
            message=message,
            status_code=400,
            details=details,
        )