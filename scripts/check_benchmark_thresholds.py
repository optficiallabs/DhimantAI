"""Run the integrated benchmark and enforce configured quality thresholds."""

from __future__ import annotations

import json
from pathlib import Path

from src.benchmark_runner import calculate_metrics, load_jsonl, run_benchmark
from src.benchmark_thresholds import evaluate_thresholds
from src.integrated_evaluator import evaluate_case

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "benchmarks" / "education_cybersecurity_cases.jsonl"
CONFIG = ROOT / "config" / "benchmark_thresholds.json"


def main() -> int:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    cases = load_jsonl(BENCHMARK)
    results = run_benchmark(cases, evaluate_case)
    metrics = calculate_metrics(results)
    gate = evaluate_thresholds(
        metrics,
        minimum_accuracy=float(config.get("minimum_accuracy", 1.0)),
        category_minimums=config.get("category_minimums") or {},
    )
    payload = {"metrics": metrics, "thresholds": gate.to_dict()}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if gate.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
