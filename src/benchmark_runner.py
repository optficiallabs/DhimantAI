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


def run_benchmark(cases: Iterable[dict], evaluator: Callable[[dict], str]) -> list[dict]:
    """Run an evaluator against benchmark cases and capture expected/actual decisions."""
    results: list[dict] = []
    for case in cases:
        actual = evaluator(case)
        expected = case.get("expected_decision")
        results.append({
            "id": case.get("id"),
            "category": case.get("category"),
            "expected_decision": expected,
            "actual_decision": actual,
            "correct": actual == expected,
        })
    return results


def calculate_metrics(results: Iterable[dict]) -> dict:
    """Calculate overall and per-category accuracy for benchmark results."""
    rows = list(results)
    total = len(rows)
    correct = sum(1 for row in rows if row.get("correct") is True)
    categories: dict[str, dict[str, int | float]] = {}
    for row in rows:
        category = str(row.get("category") or "uncategorised")
        bucket = categories.setdefault(category, {"total": 0, "correct": 0, "accuracy": 0.0})
        bucket["total"] += 1
        if row.get("correct") is True:
            bucket["correct"] += 1
    for bucket in categories.values():
        bucket["accuracy"] = bucket["correct"] / bucket["total"] if bucket["total"] else 0.0
    return {
        "total": total,
        "correct": correct,
        "incorrect": total - correct,
        "accuracy": correct / total if total else 0.0,
        "categories": categories,
    }


def expected_decision_evaluator(case: dict) -> str:
    """Reference evaluator used to validate benchmark runner plumbing."""
    return str(case.get("expected_decision", "review"))
