# Decisions Log
_Append-only. Never edit or delete existing entries. Always add new entries at the bottom._

---

### 2026-03-31

**Decision:** Use OpenClaw over Wati/Interakt
**Reason:** Free, self-hosted, no monthly subscription. Unofficial Baileys
protocol is acceptable risk for a single-store deployment on a dedicated SIM.

**Decision:** Gemini 1.5 Flash (free) for simple turns, Claude Sonnet for complex
**Reason:** ~90% of bot turns are simple (greetings, button confirmations,
step transitions). Gemini handles these for free. Claude only called for
medicine fuzzy search, ambiguous queries, and prescription reading.

**Decision:** EvitalRX API not used — Google Sheets instead
**Reason:** EvitalRX API only available on higher plans. Basic plan has no API
access. Google Sheets is free, editable from phone, and readable via gspread.
When/if EvitalRX plan is upgraded, swap is a one-file change in inventory.py.

**Decision:** Google Sheets over SQLite for inventory
**Reason:** Stock levels need to be updated by the owner throughout the day.
Google Sheets is editable from any phone/browser without technical knowledge.
SQLite for orders only (read by bot, written by bot — no manual edits needed).

**Decision:** Cloudflare Tunnel over port forwarding or ngrok
**Reason:** Free, stable, no time limits, no bandwidth caps, no account
required for basic use. More reliable than ngrok free tier.

**Decision:** Dedicated Jio SIM for bot WhatsApp number
**Reason:** OpenClaw uses unofficial Baileys protocol. Separating bot number
from personal number reduces ban risk and keeps business communication clean.

### 2026-03-31 (updated)
**Decision:** Two separate NIM API keys
**Reason:** Key 1 for OpenClaw agent brain, Key 2 for FastAPI backend.
Separate rate limit buckets. Independent credit tracking on build.nvidia.com.
Both keys stored only in .env — never committed to GitHub.
.env is in .gitignore — confirmed safe.

### 2026-03-31 (updated 2)
**Decision:** Use NVIDIA NIM (Llama 3.1/3.3) via OpenClaw as primary LLM
**Reason:** Higher accuracy than Gemini Flash, better control vs Claude cost.
OpenClaw acts as orchestration layer. Latency (~3–5s) acceptable for pharmacy use.

**Decision:** Use OpenClaw UI only for debugging, not production
**Reason:** UI introduces tool overhead and latency. Production system will call
OpenClaw or backend APIs directly (FastAPI), not rely on UI sessions.