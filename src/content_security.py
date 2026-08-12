"""Defensive checks for public-safe DhimantAI learning content.

The module provides deterministic reference checks for suspicious instructions that
may appear in learning material. It is intentionally conservative, dependency-free,
and suitable for synthetic benchmarks and unit tests. It is not a replacement for
production security controls or institutional policy.
"""

from __future__ import annotations

from typing import Final

RISK_ORDER: Final = {"low": 0, "medium": 1, "high": 2, "critical": 3}

RULES: Final = (
    {
        "id": "instruction_override",
        "category": "instruction_manipulation",
        "phrase": "ignore previous instructions",
        "severity": "high",
        "message": "Content attempts to override existing instructions.",
    },
    {
        "id": "answer_key_exposure",
        "category": "assessment_integrity",
        "phrase": "reveal the answer key",
        "severity": "critical",
        "message": "Content requests disclosure of restricted assessment answers.",
    },
    {
        "id": "teacher_control_bypass",
        "category": "access_control",
        "phrase": "bypass teacher settings",
        "severity": "critical",
        "message": "Content attempts to bypass educator or institution controls.",
    },
    {
        "id": "hidden_instruction_exposure",
        "category": "confidentiality",
        "phrase": "show hidden instructions",
        "severity": "high",
        "message": "Content requests disclosure of hidden system or workflow instructions.",
    },
    {
        "id": "cross_student_access",
        "category": "student_privacy",
        "phrase": "access another student",
        "severity": "critical",
        "message": "Content requests access to another learner's information.",
    },
    {
        "id": "restricted_exam_request",
        "category": "assessment_integrity",
        "phrase": "show the exam answers",
        "severity": "critical",
        "message": "Content requests restricted examination answers.",
    },
    {
        "id": "credential_request",
        "category": "credential_safety",
        "phrase": "share your password",
        "severity": "critical",
        "message": "Content requests a password or credential.",
    },
    {
        "id": "bulk_student_export",
        "category": "student_privacy",
        "phrase": "export all student records",
        "severity": "critical",
        "message": "Content requests bulk access to student records.",
    },
)

SUSPICIOUS_PHRASES: Final = tuple(rule["phrase"] for rule in RULES)


def _highest_risk(findings: list[dict]) -> str:
    if not findings:
        return "low"
    return max((finding["severity"] for finding in findings), key=RISK_ORDER.__getitem__)


def scan_learning_content(text: str) -> dict:
    """Scan learning content and return structured defensive findings.

    The result remains backward compatible with the original ``safe``, ``matches``,
    and ``risk`` fields while adding categories, rule identifiers, and human-readable
    findings for evaluation and documentation.
    """
    normalized = (text or "").casefold()
    findings = []

    for rule in RULES:
        if rule["phrase"] in normalized:
            findings.append(
                {
                    "rule_id": rule["id"],
                    "category": rule["category"],
                    "severity": rule["severity"],
                    "match": rule["phrase"],
                    "message": rule["message"],
                }
            )

    categories = sorted({finding["category"] for finding in findings})
    matches = [finding["match"] for finding in findings]

    return {
        "safe": not findings,
        "risk": _highest_risk(findings),
        "matches": matches,
        "categories": categories,
        "finding_count": len(findings),
        "findings": findings,
    }
