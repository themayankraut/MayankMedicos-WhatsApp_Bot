# backend/main.py
# WhatsApp Medical Store Bot — Main FastAPI Server
# Receives messages from OpenClaw, routes to NIM, sends reply back

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

from backend.ai_router import call_simple, call_complex
from backend.conversation import get_session, update_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def root():
    return {"status": "MedStore Bot running", "phase": 1}


@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        logger.info(f"Incoming: {data}")

        # OpenClaw sends messages in this format
        message_text = data.get("message", "")
        sender        = data.get("sender", "unknown")

        if not message_text:
            return JSONResponse({"reply": ""})

        # Get or create session for this patient
        session = get_session(sender)

        # Route to correct NIM model based on session step
        if session.get("step") in ["medicine_search"]:
            reply = await call_complex(
                prompt=message_text,
                system="You are a helpful pharmacy assistant. Reply concisely."
            )
        else:
            reply = await call_simple(
                prompt=message_text,
                system="You are a helpful pharmacy assistant. Reply concisely."
            )

        # Update session
        update_session(sender, {"last_message": message_text})

        logger.info(f"Reply to {sender}: {reply}")
        return JSONResponse({"reply": reply})

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return JSONResponse({"reply": "Sorry, something went wrong. Please try again."})