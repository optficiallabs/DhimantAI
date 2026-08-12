# Benchmark Reporting

DhimantAI can generate reproducible benchmark reports from the structured education cybersecurity benchmark.

## Outputs

The report generator writes two files:

- JSON for machine-readable metrics, decision matrices, failed-case diagnostics, and per-case traces.
- Markdown for human review in CI, pull requests, research notes, and release validation.

## Metrics

Reports include:

- total, correct, and incorrect case counts
- overall accuracy
- per-category accuracy
- actual and expected decision counts
- expected-vs-actual decision matrix
- compact diagnostics for failed cases

## Command

```bash
dhimantai generate-benchmark-report benchmarks/education_cybersecurity_cases.jsonl --output-dir artifacts/benchmark
```

An alternate filename stem can be supplied with `--stem`.

## CI

The `Benchmark Report` GitHub Actions workflow runs on pull requests to `main` and on manual dispatch. It evaluates the public-safe benchmark and uploads the generated JSON and Markdown files as the `dhimantai-benchmark-report` artifact.

## Safety and Scope

Benchmark reporting must use synthetic, independently created, properly licensed, or otherwise public-safe material. Generated artifacts must not contain identifiable student information, confidential institution records, credentials, restricted examination material, or production secrets.
