# backend/conversation.py
# Manages per-patient conversation state (in-memory for Phase 1)
# Phase 2 will move this to SQLite for persistence across restarts

_sessions: dict = {}


def get_session(sender: str) -> dict:
    """Get existing session or create a new one."""
    if sender not in _sessions:
        _sessions[sender] = {
            "step": "start",
            "language": None,
            "name": None,
            "cart": [],
            "delivery_date": None,
            "delivery_slot": None,
            "address": None,
        }
    return _sessions[sender]


def update_session(sender: str, updates: dict) -> dict:
    """Merge updates into existing session."""
    session = get_session(sender)
    session.update(updates)
    _sessions[sender] = session
    return session


def clear_session(sender: str):
    """Clear session after order is placed."""
    if sender in _sessions:
        del _sessions[sender]