"""Validation helpers for DhimantAI public benchmark records."""

from __future__ import annotations

REQUIRED_FIELDS = {
    "id",
    "category",
    "scenario",
    "expected_decision",
    "expected_reason",
    "human_review",
}

ALLOWED_DECISIONS = {"allow", "deny", "block", "hold", "review", "redact"}


def validate_benchmark_case(case: dict) -> list[str]:
    """Return validation errors for a single benchmark record."""
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS.difference(case))
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")

    decision = case.get("expected_decision")
    if decision is not None and decision not in ALLOWED_DECISIONS:
        errors.append(f"unsupported expected_decision: {decision}")

    if "human_review" in case and not isinstance(case["human_review"], bool):
        errors.append("human_review must be boolean")

    if not str(case.get("id", "")).startswith("EDU-"):
        errors.append("id must start with EDU-")

    return errors


def summarise_cases(cases: list[dict]) -> dict:
    """Return simple reproducibility metadata for a benchmark collection."""
    categories: dict[str, int] = {}
    review_count = 0
    for case in cases:
        category = str(case.get("category", "unknown"))
        categories[category] = categories.get(category, 0) + 1
        review_count += int(bool(case.get("human_review", False)))

    return {
        "total_cases": len(cases),
        "categories": categories,
        "human_review_cases": review_count,
    }
