"""Privacy-aware logging helpers for synthetic/public-safe DhimantAI examples."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

DEFAULT_REDACTION = "[REDACTED]"

SENSITIVE_FIELDS = {
    "student_name",
    "student_email",
    "student_id",
    "phone",
    "address",
    "date_of_birth",
    "guardian_name",
    "guardian_phone",
    "institution_id",
    "password",
    "token",
    "api_key",
    "secret",
}


def _normalise_fields(fields: set[str] | None) -> set[str]:
    source = SENSITIVE_FIELDS if fields is None else fields
    return {str(field).strip().lower() for field in source}


def redact_value(
    value,
    *,
    sensitive_fields: set[str] | None = None,
    replacement: str = DEFAULT_REDACTION,
):
    """Recursively redact sensitive keys from mappings and nested structures.

    This helper is intended for logs, examples, test fixtures, and other
    public-safe representations. It does not modify the original object.
    """
    fields = _normalise_fields(sensitive_fields)

    if isinstance(value, Mapping):
        redacted = {}
        for key, item in value.items():
            key_text = str(key)
            if key_text.strip().lower() in fields:
                redacted[key] = replacement
            else:
                redacted[key] = redact_value(
                    item,
                    sensitive_fields=fields,
                    replacement=replacement,
                )
        return redacted

    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        redacted_items = [
            redact_value(item, sensitive_fields=fields, replacement=replacement)
            for item in value
        ]
        return tuple(redacted_items) if isinstance(value, tuple) else redacted_items

    return value


def redact_record(
    record: dict,
    sensitive_fields: set[str] | None = None,
    replacement: str = DEFAULT_REDACTION,
) -> dict:
    """Return a redacted copy of a structured log record."""
    return redact_value(
        record,
        sensitive_fields=sensitive_fields,
        replacement=replacement,
    )


def prepare_log_event(
    event_type: str,
    record: dict,
    *,
    sensitive_fields: set[str] | None = None,
    replacement: str = DEFAULT_REDACTION,
) -> dict:
    """Build a public-safe structured log event without exposing sensitive fields."""
    return {
        "event_type": str(event_type),
        "data": redact_record(
            record,
            sensitive_fields=sensitive_fields,
            replacement=replacement,
        ),
    }
