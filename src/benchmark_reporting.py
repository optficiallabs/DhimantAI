"""Benchmark report generation helpers for DhimantAI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .benchmark_runner import calculate_metrics


def decision_matrix(results: Iterable[dict]) -> dict[str, dict[str, int]]:
    """Build an expected-vs-actual decision count matrix."""
    matrix: dict[str, dict[str, int]] = {}
    for row in results:
        expected = str(row.get("expected_decision") or "unknown")
        actual = str(row.get("actual_decision") or "unknown")
        bucket = matrix.setdefault(expected, {})
        bucket[actual] = bucket.get(actual, 0) + 1
    return matrix


def failed_cases(results: Iterable[dict]) -> list[dict]:
    """Return compact diagnostics for benchmark cases that did not match expectations."""
    failures: list[dict] = []
    for row in results:
        if row.get("correct") is True:
            continue
        evaluation = row.get("evaluation") or {}
        failures.append(
            {
                "id": row.get("id"),
                "category": row.get("category"),
                "expected_decision": row.get("expected_decision"),
                "actual_decision": row.get("actual_decision"),
                "module": evaluation.get("module"),
                "reason": evaluation.get("reason"),
            }
        )
    return failures


def build_report(results: Iterable[dict]) -> dict:
    """Build a machine-readable benchmark report."""
    rows = list(results)
    return {
        "metrics": calculate_metrics(rows),
        "decision_matrix": decision_matrix(rows),
        "failed_cases": failed_cases(rows),
        "results": rows,
    }


def render_markdown(report: dict, title: str = "DhimantAI Benchmark Report") -> str:
    """Render a concise Markdown report suitable for CI artifacts and review."""
    metrics = report.get("metrics") or {}
    matrix = report.get("decision_matrix") or {}
    failures = report.get("failed_cases") or []
    categories = metrics.get("categories") or {}

    lines = [
        f"# {title}",
        "",
        "## Summary",
        "",
        f"- Total cases: {metrics.get('total', 0)}",
        f"- Correct: {metrics.get('correct', 0)}",
        f"- Incorrect: {metrics.get('incorrect', 0)}",
        f"- Accuracy: {float(metrics.get('accuracy', 0.0)):.2%}",
        "",
        "## Category Accuracy",
        "",
        "| Category | Correct | Total | Accuracy |",
        "|---|---:|---:|---:|",
    ]
    for category in sorted(categories):
        bucket = categories[category]
        lines.append(
            f"| {category} | {bucket.get('correct', 0)} | {bucket.get('total', 0)} | {float(bucket.get('accuracy', 0.0)):.2%} |"
        )

    decisions = sorted({decision for expected in matrix.values() for decision in expected} | set(matrix))
    lines.extend(["", "## Decision Matrix", ""])
    if decisions:
        lines.append("| Expected \\ Actual | " + " | ".join(decisions) + " |")
        lines.append("|---|" + "---:|" * len(decisions))
        for expected in decisions:
            bucket = matrix.get(expected, {})
            lines.append("| " + expected + " | " + " | ".join(str(bucket.get(actual, 0)) for actual in decisions) + " |")
    else:
        lines.append("No decisions recorded.")

    lines.extend(["", "## Failed Cases", ""])
    if failures:
        lines.append("| ID | Category | Expected | Actual | Module | Reason |")
        lines.append("|---|---|---|---|---|---|")
        for failure in failures:
            values = [
                failure.get("id"),
                failure.get("category"),
                failure.get("expected_decision"),
                failure.get("actual_decision"),
                failure.get("module"),
                failure.get("reason"),
            ]
            safe = [str(value or "").replace("|", "\\|") for value in values]
            lines.append("| " + " | ".join(safe) + " |")
    else:
        lines.append("No failed cases.")

    return "\n".join(lines) + "\n"


def write_report_files(report: dict, output_dir: str | Path, stem: str = "benchmark-report") -> dict[str, str]:
    """Write JSON and Markdown report files and return their paths."""
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    json_path = directory / f"{stem}.json"
    markdown_path = directory / f"{stem}.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(report), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(markdown_path)}
