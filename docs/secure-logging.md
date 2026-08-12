# Secure Logging and Redaction

DhimantAI public examples should avoid exposing identifiable student information, institution identifiers, credentials, and other sensitive fields.

The reference helper in `src/secure_logging.py` provides recursive redaction for structured log records. It supports nested dictionaries, lists and tuples, case-insensitive field matching, configurable sensitive-field sets, and configurable replacement text.

## Default protected fields

The reference list includes common student, guardian, institution, credential and secret-related fields such as `student_name`, `student_email`, `student_id`, `phone`, `address`, `date_of_birth`, `guardian_name`, `institution_id`, `password`, `token`, `api_key`, and `secret`.

## Example

```python
from src.secure_logging import prepare_log_event

event = prepare_log_event(
    "lesson_opened",
    {
        "student_id": "SYN-001",
        "topic": "Algebra",
    },
)
```

The returned event retains the operational field `topic` while replacing the student identifier with `[REDACTED]`.

## Custom rules

Applications may supply their own sensitive-field set and replacement marker. This is useful where an institution has additional internal identifiers that should not appear in logs.

## Scope

This module is a small reference implementation for safe examples and development workflows. Production systems should additionally apply data minimisation, access control, retention limits, encryption, audit policy, and organisation-specific privacy requirements.
