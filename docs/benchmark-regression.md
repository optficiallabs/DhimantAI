# Benchmark Regression Tracking

DhimantAI keeps a reviewed reference baseline for the education cybersecurity benchmark and compares every pull request against it.

The regression gate checks:

- overall benchmark accuracy delta
- per-category accuracy deltas
- baseline cases that become newly incorrect
- decision changes for existing baseline cases
- baseline cases that disappear from the benchmark
- new benchmark cases and whether they pass

The current policy is stored in `config/benchmark_regression.json`. The reviewed baseline is stored in `benchmarks/baselines/education_cybersecurity_v0.3.0.json`.

The default policy allows no reduction in overall or category-level accuracy. Missing baseline cases fail closed, and newly added cases must pass before the regression gate can succeed.

Run locally:

```bash
python scripts/check_benchmark_regressions.py
```

A baseline should not be updated merely to make a failing pull request pass. Update it only after maintainers have reviewed intended benchmark or policy changes, confirmed that the new behaviour is correct, and documented why the reference result should change.
