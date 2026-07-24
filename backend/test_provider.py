import asyncio

from app.ai.providers.factory import get_llm_provider
from app.core.config import settings


async def main():
    provider = get_llm_provider(settings)

    print(f"Provider : {provider.provider_name}")
    print(f"Model    : {provider.model_name}")
    print("-" * 50)

    response = await provider.generate_text(
        system_prompt="You are a helpful AI assistant.",
        user_prompt="Reply with only the word Hello.",
    )

    print("Response:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())