"""Run DhimantAI benchmark regression checks against the reviewed baseline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.benchmark_regression import compare_to_baseline
from src.benchmark_runner import calculate_metrics, load_jsonl, run_benchmark
from src.integrated_evaluator import evaluate_case

BENCHMARK = ROOT / "benchmarks" / "education_cybersecurity_cases.jsonl"
CONFIG = ROOT / "config" / "benchmark_regression.json"


def main() -> int:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    baseline_path = ROOT / str(config["baseline"])
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))

    cases = load_jsonl(BENCHMARK)
    results = run_benchmark(cases, evaluate_case)
    metrics = calculate_metrics(results)
    regression = compare_to_baseline(
        results,
        metrics,
        baseline,
        maximum_accuracy_drop=float(config.get("maximum_accuracy_drop", 0.0)),
        maximum_category_drop=float(config.get("maximum_category_drop", 0.0)),
        fail_on_new_case_failure=bool(config.get("fail_on_new_case_failure", True)),
        fail_on_missing_baseline_case=bool(config.get("fail_on_missing_baseline_case", True)),
    )

    print(json.dumps({"metrics": metrics, "regression": regression.to_dict()}, indent=2, sort_keys=True))
    return 0 if regression.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
