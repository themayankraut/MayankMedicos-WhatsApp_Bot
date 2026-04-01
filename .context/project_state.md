# Project State
**Last updated:** 2026-03-31 · Claude (synced after ChatGPT session)
**Current phase:** 1 — Foundation

---

## Current Stack
| Layer | Tool | Status |
|---|---|---|
| WhatsApp Gateway | OpenClaw (Baileys) on WSL | ✅ Installed & working |
| Internet Tunnel | Cloudflare Tunnel | ❌ Not set up yet |
| Backend | Python FastAPI | ❌ Files created, not written yet |
| AI — Primary | NVIDIA NIM — Llama 3.1 8B (simple) + Llama 3.3 70B (complex) | ✅ Working via OpenClaw |
| AI — Fallback (optional) | Gemini 1.5 Flash / Claude Sonnet | ⏳ Not configured yet |
| Inventory | Google Sheets | ❌ Sheet not created yet |
| Orders | SQLite (local) | ❌ Not set up yet |
| IDE | Google Antigravity | ✅ Active |

---

## Last Completed Task
OpenClaw installed on WSL. NVIDIA NIM (Llama 3.1/3.3) integrated and
confirmed working via OpenClaw UI. Dual NIM API keys configured — Key 1
for OpenClaw brain, Key 2 for FastAPI backend. openclaw.json fixed after
auth.profiles error. Project folder structure and all base files created.
Pushed to GitHub.

---

## Next Immediate Step
1. Set up Cloudflare Tunnel (exposes local PC to internet)
2. Build backend/main.py — FastAPI /webhook endpoint
3. Connect OpenClaw → FastAPI webhook
4. Create Google Sheets inventory (Medicines, Surgical, BabyFood, Cosmetics tabs)
5. Write backend/inventory.py (reads stock from Google Sheet)
6. Test end-to-end: patient sends WhatsApp message → NIM processes → reply sent

---

## Current Blockers
- Cloudflare Tunnel not set up — bot not reachable from internet yet
- Google Sheet inventory not created
- FastAPI backend code not written yet
- Gemini/Claude API keys not obtained (not blocking — NIM is primary)

---

## File Map
```
whatsapp-medstore-bot/
  .context/
    project_state.md       ← this file
    decisions_log.md       ← why each decision was made
    handover_template.md   ← copy-paste when switching AIs
  backend/
    main.py                ← FastAPI app (not written yet)
    ai_router.py           ← NIM Llama routing — simple vs complex turns
    conversation.py        ← session state per patient (not written yet)
    inventory.py           ← Google Sheets stock reads (not written yet)
    delivery.py            ← delivery window logic (not written yet)
    orders.py              ← SQLite order saving (not written yet)
  .env                     ← secrets (not on GitHub — in .gitignore)
  .gitignore
  requirements.txt
```

---

## Known Issues / Notes
- EvitalRX API only on higher plan → using Google Sheets as inventory.
  Manual EvitalRX entry for billing by owner. Swap is one-file change later.
- OpenClaw uses unofficial WhatsApp Baileys protocol. Dedicated Jio SIM only.
- OpenClaw UI used for debugging only. Production calls go FastAPI → NIM directly.
- NIM free credits (1,000 per key × 2 keys = 2,000 total) cover full dev + testing.
- openclaw.json contains sensitive tokens — must never be committed to GitHub.