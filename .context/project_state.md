# Project State
**Last updated:** 2026-03-31 · Claude
**Current phase:** 1 — Foundation

---

## Current Stack
| Layer | Tool | Status |
|---|---|---|
| WhatsApp Gateway | OpenClaw (Baileys) | Installed & working |
| Internet Tunnel | Cloudflare Tunnel | Not set up yet |
| Backend | Python FastAPI | Files created, not written yet |
| AI — Primary | NVIDIA NIM (Llama 3.1/3.3 via OpenClaw) | Working |
| AI — Secondary (optional) | Gemini / Claude | Not configured |
| Inventory | Google Sheets | Sheet not created yet |
| Orders | SQLite (local) | Not set up yet |
| IDE | Google Antigravity | Active |

---

## Last Completed Task
Project folder structure created. OpenClaw installed and configured on WSL.
NVIDIA NIM integrated and working via OpenClaw UI.

## Next Immediate Step
## Next Immediate Step
1. Build FastAPI backend (/webhook endpoint)
2. Connect OpenClaw → FastAPI
3. Create Google Sheets inventory
4. Implement inventory.py (read stock)
5. Test end-to-end flow (message → AI → response)


## Current Blockers
- Gemini API key not yet obtained
- Claude API key not yet obtained
- Google Sheet not yet created
- OpenClaw not yet installed
- EvitalRX API not available on basic plan
  → Using Google Sheets as inventory replacement

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
    ai_router.py           ← Gemini vs Claude routing (not written yet)
    conversation.py        ← session state (not written yet)
    inventory.py           ← Google Sheets reads (not written yet)
    delivery.py            ← delivery window logic (not written yet)
    orders.py              ← SQLite order saving (not written yet)
  .env                     ← secrets (not on GitHub)
  .gitignore
  requirements.txt
```

---

## Known Issues / Notes
- EvitalRX API only on higher plan. Basic plan = no API access.
  Decision: Google Sheets mirrors stock. Manual EvitalRX entry for billing.
- OpenClaw uses unofficial WhatsApp Baileys protocol. Use dedicated SIM only.
- Gemini 1.5 Flash free tier may use prompts for training. Acceptable for
  simple turns (no patient data in those prompts). Switch to paid if needed.