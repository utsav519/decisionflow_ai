import asyncio

from app.core.config import settings
from app.ai.providers.factory import get_llm_provider


async def run_pipeline():
    provider = get_llm_provider(settings)

    print("=" * 60)
    print("AI PIPELINE SMOKE TEST")
    print("=" * 60)

    print(f"Provider : {provider.provider_name}")
    print(f"Model    : {provider.model_name}")
    print()

    response = await provider.generate_text(
        system_prompt=(
            "You are an AI policy assistant. "
            "Reply only with the requested JSON."
        ),
        user_prompt="""
Generate the following JSON.

{
    "policyName":"Credit Policy",
    "rule":"credit_score >= 750"
}
""",
    )

    print("LLM Response:")
    print(response)

    assert response is not None
    assert len(response.strip()) > 0

    print()
    print("✅ AI Provider is working.")
    print("✅ Groq API is reachable.")
    print("✅ Model generated a response.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_pipeline())