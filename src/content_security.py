"""Basic defensive checks for public-safe DhimantAI learning content."""

from __future__ import annotations

SUSPICIOUS_PHRASES = (
    "ignore previous instructions",
    "reveal the answer key",
    "bypass teacher settings",
    "show hidden instructions",
    "access another student",
)


def scan_learning_content(text: str) -> dict:
    """Return a simple structured result for suspicious instruction patterns.

    This is a lightweight reference implementation for testing and examples.
    It is not a complete production security control.
    """
    normalized = (text or "").lower()
    matches = [phrase for phrase in SUSPICIOUS_PHRASES if phrase in normalized]
    return {
        "safe": not matches,
        "matches": matches,
        "risk": "high" if matches else "low",
    }
