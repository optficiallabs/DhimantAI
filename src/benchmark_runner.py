"""Benchmark execution and metric helpers for DhimantAI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Iterable


def load_jsonl(path: str | Path) -> list[dict]:
    """Load non-empty JSONL records from a benchmark file."""
    records: list[dict] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                record = json.loads(text)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"Benchmark line {line_number} must contain an object")
            records.append(record)
    return records


def run_benchmark(cases: Iterable[dict], evaluator: Callable[[dict], str | dict]) -> list[dict]:
    """Run an evaluator and capture expected/actual decisions plus optional trace."""
    results: list[dict] = []
    for case in cases:
        evaluation = evaluator(case)
        if isinstance(evaluation, dict):
            actual = str(evaluation.get("decision") or "review")
            trace = evaluation
        else:
            actual = str(evaluation)
            trace = None
        expected = case.get("expected_decision")
        row = {
            "id": case.get("id"),
            "category": case.get("category"),
            "expected_decision": expected,
            "actual_decision": actual,
            "correct": actual == expected,
        }
        if trace is not None:
            row["evaluation"] = trace
        results.append(row)
    return results


def calculate_metrics(results: Iterable[dict]) -> dict:
    """Calculate accuracy, decision counts, and per-category accuracy."""
    rows = list(results)
    total = len(rows)
    correct = sum(1 for row in rows if row.get("correct") is True)
    categories: dict[str, dict[str, int | float]] = {}
    decisions: dict[str, int] = {}
    expected_decisions: dict[str, int] = {}

    for row in rows:
        category = str(row.get("category") or "uncategorised")
        bucket = categories.setdefault(category, {"total": 0, "correct": 0, "accuracy": 0.0})
        bucket["total"] += 1
        if row.get("correct") is True:
            bucket["correct"] += 1
        actual = str(row.get("actual_decision") or "unknown")
        expected = str(row.get("expected_decision") or "unknown")
        decisions[actual] = decisions.get(actual, 0) + 1
        expected_decisions[expected] = expected_decisions.get(expected, 0) + 1

    for bucket in categories.values():
        bucket["accuracy"] = bucket["correct"] / bucket["total"] if bucket["total"] else 0.0

    return {
        "total": total,
        "correct": correct,
        "incorrect": total - correct,
        "accuracy": correct / total if total else 0.0,
        "coverage": 1.0 if total else 0.0,
        "decision_counts": decisions,
        "expected_decision_counts": expected_decisions,
        "categories": categories,
    }


def expected_decision_evaluator(case: dict) -> str:
    """Reference evaluator used only to validate benchmark runner plumbing."""
    return str(case.get("expected_decision", "review"))
