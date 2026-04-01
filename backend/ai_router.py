# backend/ai_router.py
# Handles all AI model calls — routes to correct model based on message type
# Uses NVIDIA_NIM_API_KEY_BACKEND from .env

import os
import re
from openai import AsyncOpenAI
from dotenv import load_dotenv
from backend.conversation import get_session

load_dotenv()

# NIM is OpenAI-compatible — use the OpenAI client pointed at NIM's URL
nim_client = AsyncOpenAI(
    api_key=os.getenv("NVIDIA_NIM_API_KEY_BACKEND"),
    base_url="https://integrate.api.nvidia.com/v1"
)

SIMPLE_MODEL  = "meta/llama-3.1-8b-instruct"   # greetings, simple questions
COMPLEX_MODEL = "meta/llama-3.3-70b-instruct"   # medicine search, Hindi parsing, ambiguous queries

STORE_NAME  = os.getenv("STORE_NAME", "Mayank Medicos")
OWNER_PHONE = os.getenv("STORE_OWNER_PHONE", "")

# ── System Prompts ─────────────────────────────────────────────────────────────

PHARMACY_SYSTEM_PROMPT = f"""You are the WhatsApp assistant for {STORE_NAME}, a local pharmacy and medical store in India.

Your ONLY job is to help customers with:
- Checking medicine availability (e.g. "Do you have Dolo 650?")
- Providing medicine prices and pack sizes
- Taking medicine orders
- Answering questions about delivery timing
- Basic pharmacy-related questions (dosages, alternatives, generics)

Rules you MUST follow:
1. ALWAYS reply in the same language the customer used. If they write in Hindi (Devanagari or Roman Hindi), reply in Hindi. If in English, reply in English.
2. NEVER answer questions that are NOT related to medicines, pharmacy, or health products. If someone asks something off-topic (jokes, relationships, general knowledge, entertainment), politely say: "मैं सिर्फ Mayank Medicos की दवाइयों के बारे में मदद कर सकता हूँ। / I can only help with medicines and pharmacy queries at {STORE_NAME}."
3. NEVER reveal that you are an AI, a bot, or powered by any specific technology.
4. Keep replies SHORT and helpful — maximum 3-4 sentences.
5. If you don't know the exact stock or price, say: "Please call the store to confirm availability."
6. Greet new customers warmly. Use their name if known.
7. For orders, collect: medicine name, quantity, customer name, and delivery address.

Store hours: 9 AM – 9 PM, Monday to Saturday.
Same-day delivery cutoff: 4 PM.
"""

GREETING_PROMPT = f"""You are the WhatsApp assistant for {STORE_NAME}, a local pharmacy.
Give a warm, brief welcome message in 1-2 sentences.
Ask how you can help with their medicine or healthcare needs today.
If they wrote in Hindi, reply in Hindi. If in English, reply in English.
Do NOT mention you are a bot or AI."""


# ── Routing Logic ──────────────────────────────────────────────────────────────

# Keywords that suggest this is a simple greeting, not a complex query
GREETING_PATTERNS = re.compile(
    r"^\s*(hi|hello|hey|hii|helo|namaste|namaskar|jai hind|good morning|good afternoon|"
    r"good evening|good night|हेलो|नमस्ते|हाय|शुभ|ok|okay|thanks|thank you|धन्यवाद|ठीक है)\s*[!?.]?\s*$",
    re.IGNORECASE
)

# Keywords that force the complex (70B) model
COMPLEX_KEYWORDS = re.compile(
    r"(medicine|tablet|capsule|syrup|injection|cream|ointment|drop|strip|dose|dosage|"
    r"mg|ml|generic|brand|alternative|substitute|price|cost|rate|stock|available|"
    r"दवा|दवाई|टेबलेट|कैप्सूल|सिरप|क्रीम|इंजेक्शन|दाम|कीमत|उपलब्ध|खुराक)",
    re.IGNORECASE
)


def _choose_model(message: str, session: dict) -> tuple[str, str]:
    """Choose the right model and system prompt based on message content."""
    msg = message.strip()

    # Simple greeting → use fast 8B model
    if GREETING_PATTERNS.match(msg):
        return SIMPLE_MODEL, GREETING_PROMPT

    # Medicine/complex query → use powerful 70B model
    if COMPLEX_KEYWORDS.search(msg):
        return COMPLEX_MODEL, PHARMACY_SYSTEM_PROMPT

    # Default: use 8B for general pharmacy chat, 70B for anything ambiguous
    # If session is new, it might be first message — safer to use pharmacy prompt
    if session.get("step") == "start" or len(msg) > 60:
        return COMPLEX_MODEL, PHARMACY_SYSTEM_PROMPT

    return SIMPLE_MODEL, PHARMACY_SYSTEM_PROMPT


async def route_message(message: str, sender: str, session: dict) -> str:
    """Main routing function — choose model, call NIM, return reply."""
    model, system_prompt = _choose_model(message, session)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": message},
    ]

    # Add conversation history from session if available
    history = session.get("history", [])
    if history:
        # Insert recent history before the current user message
        messages = (
            [{"role": "system", "content": system_prompt}]
            + history[-6:]  # only last 3 exchanges (6 messages)
            + [{"role": "user", "content": message}]
        )

    max_tokens = 256 if model == SIMPLE_MODEL else 512
    temperature = 0.7 if model == SIMPLE_MODEL else 0.3

    response = await nim_client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    reply = response.choices[0].message.content.strip()

    # Update conversation history in session
    session.setdefault("history", [])
    session["history"].append({"role": "user",      "content": message})
    session["history"].append({"role": "assistant",  "content": reply})

    return reply