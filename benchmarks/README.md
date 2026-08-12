# DhimantAI Education Cybersecurity Benchmark

This directory contains public-safe benchmark material for evaluating security controls around digital learning workflows.

The benchmark is intentionally synthetic and designed for reproducible defensive testing. It does not contain identifiable student information, confidential institution records, restricted examination material, credentials, production logs, or private third-party data.

## Current categories

- normal learning activity
- manipulated learning content
- assessment misuse
- role and permission violations
- student-data exposure risks
- institution-content integrity
- human-review cases
- multi-step workflow cases

## Record format

Each case contains:

- `id`: stable benchmark identifier
- `category`: scenario family
- `scenario`: short synthetic description
- `expected_decision`: expected security outcome
- `expected_reason`: rationale for the expected outcome
- `human_review`: whether additional authorised review is expected

Supported expected decisions in the reference validator are `allow`, `deny`, `block`, `hold`, `review`, and `redact`.

## Reproducibility

`src/benchmark_validation.py` provides basic schema validation and collection summaries. This allows contributors to check that new benchmark records use the same required fields and decision vocabulary.

The current expanded sample collection is stored in `education_cybersecurity_cases.jsonl`. It is a seed set for continued growth, not a claim that the planned research benchmark is complete.

## Data rules

All material added here must be synthetic, independently created, properly licensed, or otherwise suitable for public release. Do not add real student identifiers, institutional secrets, answer keys from restricted assessments, authentication information, or confidential logs.
