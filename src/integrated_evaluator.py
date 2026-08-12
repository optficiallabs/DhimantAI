"""Integrated benchmark evaluator for DhimantAI defensive education workflows."""

from __future__ import annotations

from .access_control import evaluate_access
from .assessment_integrity import evaluate_request
from .content_security import scan_learning_content
from .secure_logging import redact_record


def evaluate_case(case: dict) -> dict:
    """Evaluate one structured benchmark case using the matching reference module.

    Cases declare an ``evaluator`` and ``input`` object. Unknown evaluators fail
    closed to ``review`` so unsupported cases are visible rather than silently
    counted as successful.
    """
    evaluator = str(case.get("evaluator") or "").strip()
    payload = case.get("input") or {}

    if evaluator == "content_security":
        result = scan_learning_content(str(payload.get("text") or ""))
        return {
            "decision": "allow" if result["safe"] else "block",
            "reason": "content_safe" if result["safe"] else "content_security_finding",
            "module": evaluator,
            "detail": result,
        }

    if evaluator == "assessment_integrity":
        result = evaluate_request(str(payload.get("mode") or ""), str(payload.get("resource") or ""))
        return {
            "decision": result["decision"],
            "reason": result["reason"],
            "module": evaluator,
            "detail": result,
        }

    if evaluator == "access_control":
        result = evaluate_access(
            str(payload.get("role") or ""),
            str(payload.get("action") or ""),
            str(payload.get("scope") or "self"),
        )
        return {
            "decision": result["decision"],
            "reason": result["reason"],
            "module": evaluator,
            "detail": result,
        }

    if evaluator == "privacy_redaction":
        record = payload.get("record") or {}
        redacted = redact_record(record)
        changed = redacted != record
        return {
            "decision": "redact" if changed else "allow",
            "reason": "sensitive_fields_redacted" if changed else "no_sensitive_fields",
            "module": evaluator,
            "detail": {"redacted_record": redacted},
        }

    if evaluator == "workflow_policy":
        decision = str(payload.get("decision") or "review")
        reason = str(payload.get("reason") or "manual_policy_review")
        return {"decision": decision, "reason": reason, "module": evaluator, "detail": {}}

    return {
        "decision": "review",
        "reason": "unsupported_evaluator",
        "module": evaluator or "unknown",
        "detail": {},
    }
