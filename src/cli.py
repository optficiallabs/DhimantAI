"""Command-line interface for DhimantAI public-safe utilities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .access_control import evaluate_access
from .benchmark_runner import calculate_metrics, expected_decision_evaluator, load_jsonl, run_benchmark
from .content_security import scan_learning_content


def _read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dhimantai", description="DhimantAI open-source utility CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate-content", help="Scan a text or JSON file for configured content-security patterns")
    validate.add_argument("path")

    access = subparsers.add_parser("check-access", help="Evaluate a role/action/scope access request")
    access.add_argument("role")
    access.add_argument("action")
    access.add_argument("--scope", default="self")

    benchmark = subparsers.add_parser("run-benchmark", help="Run benchmark plumbing and report reproducible metrics")
    benchmark.add_argument("path")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "validate-content":
        raw = _read_text(args.path)
        try:
            parsed = json.loads(raw)
            text = json.dumps(parsed, ensure_ascii=False)
        except json.JSONDecodeError:
            text = raw
        print(json.dumps(scan_learning_content(text), indent=2, sort_keys=True))
        return 0

    if args.command == "check-access":
        print(json.dumps(evaluate_access(args.role, args.action, args.scope), indent=2, sort_keys=True))
        return 0

    if args.command == "run-benchmark":
        cases = load_jsonl(args.path)
        results = run_benchmark(cases, expected_decision_evaluator)
        print(json.dumps(calculate_metrics(results), indent=2, sort_keys=True))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
