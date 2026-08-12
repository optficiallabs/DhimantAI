"""Reference assessment-integrity rules for DhimantAI learning modes."""

from __future__ import annotations

from typing import Final

MODE_RULES: Final = {
    "guided_practice": {
        "hints": True,
        "worked_example": True,
        "final_answer_before_attempt": False,
        "answer_key": False,
    },
    "revision": {
        "hints": True,
        "worked_example": True,
        "final_answer_before_attempt": False,
        "answer_key": False,
    },
    "examination": {
        "hints": False,
        "worked_example": False,
        "final_answer_before_attempt": False,
        "answer_key": False,
    },
    "teacher_review": {
        "hints": True,
        "worked_example": True,
        "final_answer_before_attempt": True,
        "answer_key": True,
    },
}

RESOURCE_LABELS: Final = {
    "hints": "guided hints",
    "worked_example": "worked examples",
    "final_answer_before_attempt": "final answers before a learner attempt",
    "answer_key": "restricted answer keys",
}


def is_resource_allowed(mode: str, resource: str) -> bool:
    """Return whether a learning resource is permitted in the selected mode."""
    return bool(MODE_RULES.get(mode, {}).get(resource, False))


def evaluate_request(mode: str, resource: str) -> dict:
    """Return a structured assessment-integrity decision.

    Unknown modes and resources fail closed. This makes the reference behaviour
    predictable for tests and safer for education workflow examples.
    """
    mode_known = mode in MODE_RULES
    resource_known = resource in RESOURCE_LABELS
    allowed = mode_known and resource_known and is_resource_allowed(mode, resource)

    if not mode_known:
        reason = "Unknown learning mode; request denied by default."
    elif not resource_known:
        reason = "Unknown resource type; request denied by default."
    elif allowed:
        reason = f"{RESOURCE_LABELS[resource].capitalize()} are permitted in {mode}."
    else:
        reason = f"{RESOURCE_LABELS[resource].capitalize()} are restricted in {mode}."

    return {
        "mode": mode,
        "resource": resource,
        "mode_known": mode_known,
        "resource_known": resource_known,
        "allowed": allowed,
        "decision": "allow" if allowed else "deny",
        "reason": reason,
    }
