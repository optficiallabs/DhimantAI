"""Reference assessment-integrity rules for DhimantAI learning modes."""

from __future__ import annotations

MODE_RULES = {
    "guided_practice": {"hints": True, "final_answer_before_attempt": False, "answer_key": False},
    "revision": {"hints": True, "final_answer_before_attempt": False, "answer_key": False},
    "examination": {"hints": False, "final_answer_before_attempt": False, "answer_key": False},
    "teacher_review": {"hints": True, "final_answer_before_attempt": True, "answer_key": True},
}


def is_resource_allowed(mode: str, resource: str) -> bool:
    return bool(MODE_RULES.get(mode, {}).get(resource, False))


def evaluate_request(mode: str, resource: str) -> dict:
    allowed = is_resource_allowed(mode, resource)
    return {
        "mode": mode,
        "resource": resource,
        "allowed": allowed,
        "decision": "allow" if allowed else "deny",
    }
