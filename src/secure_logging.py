"""Privacy-aware logging helpers for synthetic/public-safe DhimantAI examples."""

from __future__ import annotations

SENSITIVE_FIELDS = {
    "student_name",
    "student_email",
    "student_id",
    "phone",
    "address",
    "password",
    "token",
    "api_key",
}


def redact_record(record: dict, sensitive_fields: set[str] | None = None) -> dict:
    fields = sensitive_fields or SENSITIVE_FIELDS
    redacted = {}
    for key, value in record.items():
        redacted[key] = "[REDACTED]" if key in fields else value
    return redacted
