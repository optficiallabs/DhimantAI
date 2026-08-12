# Benchmark Threshold Gates

DhimantAI uses configurable benchmark quality gates to prevent silent regressions in the public-safe evaluation suite.

The configuration is stored in `config/benchmark_thresholds.json` and can define:

- a minimum overall benchmark accuracy
- minimum accuracy requirements for selected categories

The current configuration requires 100% overall accuracy and 100% accuracy for manipulated-content, assessment-misuse, role-violation, and student-data-exposure categories. These values are intentionally strict for the small deterministic reference benchmark.

Run the gate locally with:

```bash
python scripts/check_benchmark_thresholds.py
```

The command exits with status `0` when all requirements pass and `1` when any requirement fails. Missing configured categories fail closed because the required quality level cannot be verified.

The `Benchmark Thresholds` GitHub Actions workflow runs this gate for pull requests targeting `main`.

Thresholds should only be relaxed through a reviewed change that explains why the benchmark or expected behaviour has changed.
