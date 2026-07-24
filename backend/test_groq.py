from groq import Groq

from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

response = client.chat.completions.create(
    model=settings.GROQ_MODEL,
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: Groq connection successful"
        }
    ],
)

print(response.choices[0].message.content)