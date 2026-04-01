# backend/main.py
# WhatsApp Medical Store Bot — Main Backend
# Connects to OpenClaw Gateway via WebSocket, receives messages, routes to NIM, sends reply back

import asyncio
import json
import logging
import os

import websockets
from dotenv import load_dotenv
from fastapi import FastAPI

from backend.ai_router import route_message
from backend.conversation import get_session, update_session

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
GATEWAY_URL   = os.getenv("OPENCLAW_GATEWAY_URL", "ws://127.0.0.1:18789")
GATEWAY_TOKEN = os.getenv("OPENCLAW_GATEWAY_TOKEN", "")
OWNER_PHONE   = os.getenv("STORE_OWNER_PHONE", "")

# ── FastAPI app (used for health-check endpoint only) ─────────────────────────
app = FastAPI(title="MayankMedicos Bot", version="1.0.0")


@app.get("/")
def root():
    return {"status": "MayankMedicos Bot running", "phase": 1}


@app.get("/health")
def health():
    return {"status": "ok"}


# ── OpenClaw WebSocket Client ─────────────────────────────────────────────────

async def send_reply(ws, conversation_id: str, reply: str):
    """Send a message reply back through the OpenClaw gateway."""
    payload = {
        "type": "message.send",
        "conversationId": conversation_id,
        "content": reply,
    }
    await ws.send(json.dumps(payload))
    logger.info(f"Reply sent to conversation {conversation_id}: {reply[:80]}...")


async def handle_event(ws, event: dict):
    """Process a single incoming event from OpenClaw."""
    event_type = event.get("type", "")

    # Only handle incoming messages
    if event_type not in ("message.received", "message.new"):
        return

    channel     = event.get("channel", "")
    sender      = event.get("from", event.get("sender", "unknown"))
    message_text = (
        event.get("content")
        or event.get("text")
        or event.get("message", "")
    ).strip()
    conversation_id = event.get("conversationId", event.get("sessionId", ""))

    # Only process WhatsApp messages
    if channel and "whatsapp" not in channel.lower():
        return

    if not message_text:
        return

    logger.info(f"Message from {sender}: {message_text}")

    # Get or create session
    session = get_session(sender)

    try:
        reply = await route_message(
            message=message_text,
            sender=sender,
            session=session,
        )
    except Exception as e:
        logger.error(f"AI routing error for {sender}: {e}")
        reply = "Sorry, I'm having a technical issue right now. Please try again in a moment."

    # Update session
    update_session(sender, {"last_message": message_text})

    # Send reply
    await send_reply(ws, conversation_id, reply)


async def openclaw_listener():
    """Connect to OpenClaw WebSocket gateway and listen for messages."""
    headers = {}
    if GATEWAY_TOKEN:
        headers["Authorization"] = f"Bearer {GATEWAY_TOKEN}"

    logger.info(f"Connecting to OpenClaw gateway at {GATEWAY_URL} ...")

    while True:
        try:
            async with websockets.connect(GATEWAY_URL, additional_headers=headers) as ws:
                logger.info("✅ Connected to OpenClaw gateway. Waiting for messages...")

                async for raw_message in ws:
                    try:
                        event = json.loads(raw_message)
                        await handle_event(ws, event)
                    except json.JSONDecodeError:
                        logger.warning(f"Non-JSON message received: {raw_message[:100]}")
                    except Exception as e:
                        logger.error(f"Error handling event: {e}", exc_info=True)

        except (websockets.exceptions.ConnectionClosedError,
                websockets.exceptions.ConnectionClosedOK) as e:
            logger.warning(f"Gateway connection closed: {e}. Reconnecting in 5s...")
            await asyncio.sleep(5)
        except OSError as e:
            logger.error(f"Cannot reach OpenClaw gateway: {e}. Is OpenClaw running? Retrying in 10s...")
            await asyncio.sleep(10)
        except Exception as e:
            logger.error(f"Unexpected error: {e}. Reconnecting in 5s...", exc_info=True)
            await asyncio.sleep(5)


# ── Entry point ───────────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup_event():
    """Start the OpenClaw WebSocket listener as a background task when FastAPI starts."""
    asyncio.create_task(openclaw_listener())
    logger.info("OpenClaw listener background task started.")