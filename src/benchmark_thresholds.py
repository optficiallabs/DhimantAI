"""Configurable quality gates for DhimantAI benchmark metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class ThresholdResult:
    passed: bool
    failures: tuple[str, ...]

    def to_dict(self) -> dict:
        return {"passed": self.passed, "failures": list(self.failures)}


def evaluate_thresholds(
    metrics: Mapping,
    *,
    minimum_accuracy: float = 1.0,
    category_minimums: Mapping[str, float] | None = None,
) -> ThresholdResult:
    """Evaluate overall and per-category accuracy requirements.

    Missing configured categories fail closed because the requested quality gate
    cannot be verified.
    """
    failures: list[str] = []
    overall = float(metrics.get("accuracy", 0.0))
    if overall < minimum_accuracy:
        failures.append(
            f"overall accuracy {overall:.4f} is below required {minimum_accuracy:.4f}"
        )

    categories = metrics.get("categories") or {}
    for category, required in (category_minimums or {}).items():
        if category not in categories:
            failures.append(f"required category '{category}' is missing from benchmark metrics")
            continue
        actual = float(categories[category].get("accuracy", 0.0))
        if actual < required:
            failures.append(
                f"category '{category}' accuracy {actual:.4f} is below required {float(required):.4f}"
            )

    return ThresholdResult(passed=not failures, failures=tuple(failures))
