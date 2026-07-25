from app.core.config import settings
from app.ai.providers.factory import get_llm_provider

provider = get_llm_provider(settings)

print("Provider Class :", type(provider).__name__)
print("Provider Name  :", provider.provider_name)
print("Model          :", provider.model_name)