# backend/main.py
# WhatsApp Medical Store Bot — Main FastAPI Server
# Status: Phase 1 skeleton — not functional yet
# Next step: Build /webhook endpoint and connect to ai_router.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "MedStore Bot is running", "phase": 1}

@app.post("/webhook")
async def webhook(data: dict):
    # TODO: Parse incoming OpenClaw message
    # TODO: Pass to ai_router.py
    # TODO: Return response to OpenClaw
    return {"status": "received"}
```

Press **Ctrl + S**. Repeat the same pattern for the other backend files — just add a comment at the top saying what the file will do. No actual logic yet.

---

## Setting Up the Agent Rule (One-Time Step)

This is the most useful thing you can do in Antigravity right now. Go to the bottom-right of the Editor view → click **Antigravity - Settings** → Customizations → Manage.  Add a new Rule with this content:
```
This project is a WhatsApp medical store bot for Mayank's Medical Store, Delhi.
Stack: Python FastAPI backend, OpenClaw WhatsApp gateway, Gemini 1.5 Flash for
simple turns, Claude Sonnet for complex turns, Google Sheets for inventory,
SQLite for orders, Cloudflare Tunnel for internet access.

Always read .context/project_state.md before suggesting any changes.
Never suggest changes that contradict .context/decisions_log.md.
Keep all code compatible with Python 3.10+.
Use async/await throughout the FastAPI backend.
Never hardcode API keys — always read from .env using python-dotenv.