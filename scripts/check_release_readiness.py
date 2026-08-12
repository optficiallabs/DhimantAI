"""Release-readiness checks for DhimantAI."""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "pyproject.toml",
    "docs/release-readiness.md",
]


def check_required_files() -> list[str]:
    return [path for path in REQUIRED_FILES if not (ROOT / path).exists()]


def check_project_metadata() -> list[str]:
    errors: list[str] = []
    with (ROOT / "pyproject.toml").open("rb") as handle:
        data = tomllib.load(handle)
    project = data.get("project", {})
    for field in ("name", "version", "description", "readme", "requires-python", "license"):
        if not project.get(field):
            errors.append(f"missing project metadata: {field}")
    if project.get("name") != "dhimantai":
        errors.append("project name must be dhimantai")
    return errors


def check_benchmark_records() -> list[str]:
    errors: list[str] = []
    benchmark_path = ROOT / "benchmarks" / "education_cybersecurity_cases.jsonl"
    if not benchmark_path.exists():
        return ["missing expanded education benchmark"]

    required = {
        "id",
        "category",
        "scenario",
        "expected_decision",
        "expected_reason",
        "human_review",
    }
    seen_ids: set[str] = set()
    for line_number, raw_line in enumerate(benchmark_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            case = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            errors.append(f"benchmark line {line_number}: invalid JSON: {exc.msg}")
            continue
        missing = required.difference(case)
        if missing:
            errors.append(f"benchmark line {line_number}: missing {sorted(missing)}")
        case_id = str(case.get("id", ""))
        if case_id in seen_ids:
            errors.append(f"benchmark line {line_number}: duplicate id {case_id}")
        seen_ids.add(case_id)
    return errors


def main() -> int:
    errors: list[str] = []
    missing_files = check_required_files()
    errors.extend(f"missing required file: {path}" for path in missing_files)
    errors.extend(check_project_metadata())
    errors.extend(check_benchmark_records())

    if errors:
        print("Release readiness: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Release readiness: PASSED")
    print("Required documentation, package metadata, and benchmark structure are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
