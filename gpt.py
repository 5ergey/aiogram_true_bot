import os
from openai import AsyncOpenAI
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('GPT_TOKEN')

client = AsyncOpenAI(
    base_url="https://api.proxyapi.ru/openai/v1",
    api_key=token,
)


async def gpt_text(request, content, model='gpt-4o-mini'):
    completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": content
            },
            {
                "role": "user",
                "content": request
            }
        ],
        model=model
    )
    return completion.choices[0].message.content