import asyncio

from app.core.config import settings
from app.ai.providers.factory import get_llm_provider


async def main():
    provider = get_llm_provider(settings)

    response = await provider.generate_text(
        system_prompt="You are a helpful assistant.",
        user_prompt="Reply with exactly: GroqProvider works",
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())