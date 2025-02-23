import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pyexpat.errors import messages

load_dotenv()
token = os.getenv('GPT_TOKEN')

client = AsyncOpenAI(
    base_url="https://api.proxyapi.ru/openai/v1",
    api_key=token,
)


async def gpt_text(system_content,
                   user_request,
                   ai_response='',
                   messages_list: list[dict[str, str]] = [],
                   model='gpt-3.5-turbo'
                   ):
    completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": user_request
            },
            {
                "role": "assistant",
                "content": ai_response
            }
        ] + messages_list,
        model=model
    )
    return completion.choices[0].message.content


