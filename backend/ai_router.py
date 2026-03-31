# backend/ai_router.py
# Handles all AI model calls — routes to correct model based on turn type
# Uses NVIDIA_NIM_API_KEY_BACKEND from .env

import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# NIM is OpenAI-compatible — use the OpenAI client pointed at NIM's URL
nim_client = AsyncOpenAI(
    api_key=os.getenv("NVIDIA_NIM_API_KEY_BACKEND"),
    base_url="https://integrate.api.nvidia.com/v1"
)

SIMPLE_MODEL  = "meta/llama-3.1-8b-instruct"   # greetings, buttons, Hindi
COMPLEX_MODEL = "meta/llama-3.3-70b-instruct"   # medicine search, parsing


async def call_simple(prompt: str, system: str = "") -> str:
    """For simple turns — greetings, confirmations, step transitions."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = await nim_client.chat.completions.create(
        model=SIMPLE_MODEL,
        messages=messages,
        max_tokens=512,
        temperature=0.7
    )
    return response.choices[0].message.content


async def call_complex(prompt: str, system: str = "") -> str:
    """For complex turns — medicine search, ambiguous queries, Hindi parsing."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = await nim_client.chat.completions.create(
        model=COMPLEX_MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.3   # lower = more precise for medical queries
    )
    return response.choices[0].message.content