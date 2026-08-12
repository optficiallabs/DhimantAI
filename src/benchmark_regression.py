"""Baseline comparison helpers for DhimantAI benchmark regression tracking."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RegressionResult:
    passed: bool
    accuracy_delta: float
    category_deltas: dict[str, float]
    newly_failing_cases: list[str]
    changed_decisions: list[dict]
    missing_baseline_cases: list[str]
    added_cases: list[str]
    failures: list[str]

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "accuracy_delta": self.accuracy_delta,
            "category_deltas": self.category_deltas,
            "newly_failing_cases": self.newly_failing_cases,
            "changed_decisions": self.changed_decisions,
            "missing_baseline_cases": self.missing_baseline_cases,
            "added_cases": self.added_cases,
            "failures": self.failures,
        }


def compare_to_baseline(
    results: list[dict],
    metrics: dict,
    baseline: dict,
    *,
    maximum_accuracy_drop: float = 0.0,
    maximum_category_drop: float = 0.0,
    fail_on_new_case_failure: bool = True,
    fail_on_missing_baseline_case: bool = True,
) -> RegressionResult:
    """Compare current benchmark results against a reviewed reference baseline."""
    baseline_accuracy = float(baseline.get("accuracy", 0.0))
    current_accuracy = float(metrics.get("accuracy", 0.0))
    accuracy_delta = current_accuracy - baseline_accuracy

    baseline_categories = baseline.get("categories") or {}
    current_categories = metrics.get("categories") or {}
    category_deltas: dict[str, float] = {}
    failures: list[str] = []

    if accuracy_delta < -abs(maximum_accuracy_drop):
        failures.append(
            f"overall accuracy regressed by {abs(accuracy_delta):.4f}; allowed drop is {abs(maximum_accuracy_drop):.4f}"
        )

    for category, baseline_bucket in baseline_categories.items():
        baseline_value = float((baseline_bucket or {}).get("accuracy", 0.0))
        current_bucket = current_categories.get(category)
        current_value = float((current_bucket or {}).get("accuracy", 0.0)) if current_bucket else 0.0
        delta = current_value - baseline_value
        category_deltas[category] = delta
        if delta < -abs(maximum_category_drop):
            failures.append(
                f"category {category} regressed by {abs(delta):.4f}; allowed drop is {abs(maximum_category_drop):.4f}"
            )

    baseline_cases = baseline.get("cases") or {}
    current_by_id = {str(row.get("id")): row for row in results if row.get("id") is not None}

    newly_failing_cases: list[str] = []
    changed_decisions: list[dict] = []
    missing_baseline_cases = sorted(set(baseline_cases) - set(current_by_id))
    added_cases = sorted(set(current_by_id) - set(baseline_cases))

    for case_id, baseline_case in baseline_cases.items():
        current = current_by_id.get(case_id)
        if current is None:
            continue
        baseline_correct = bool((baseline_case or {}).get("correct"))
        current_correct = bool(current.get("correct"))
        if baseline_correct and not current_correct:
            newly_failing_cases.append(case_id)
        old_decision = str((baseline_case or {}).get("decision"))
        new_decision = str(current.get("actual_decision"))
        if old_decision != new_decision:
            changed_decisions.append(
                {"id": case_id, "baseline_decision": old_decision, "current_decision": new_decision}
            )

    if fail_on_new_case_failure and newly_failing_cases:
        failures.append("newly failing baseline cases: " + ", ".join(newly_failing_cases))

    if fail_on_missing_baseline_case and missing_baseline_cases:
        failures.append("missing baseline cases: " + ", ".join(missing_baseline_cases))

    failing_added = [case_id for case_id in added_cases if not bool(current_by_id[case_id].get("correct"))]
    if fail_on_new_case_failure and failing_added:
        failures.append("new benchmark cases are failing: " + ", ".join(failing_added))

    return RegressionResult(
        passed=not failures,
        accuracy_delta=accuracy_delta,
        category_deltas=category_deltas,
        newly_failing_cases=newly_failing_cases,
        changed_decisions=changed_decisions,
        missing_baseline_cases=missing_baseline_cases,
        added_cases=added_cases,
        failures=failures,
    )
