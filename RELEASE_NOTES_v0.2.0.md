# DhimantAI v0.2.0 — Security, Benchmark and Maintainer Workflow Release

## Overview

DhimantAI v0.2.0 expands the initial open-source foundation with stronger education-workflow security controls, reproducible benchmark tooling, privacy-aware logging, release-readiness validation, and a more complete maintainer workflow.

## Highlights

- expanded learning-content security checks with structured categories, rule identifiers, findings, and severity levels
- expanded assessment-integrity policies for guided practice, revision, examination, and teacher-review modes
- fail-closed handling for unknown assessment modes and resources
- recursive privacy-aware redaction for nested student and institution records
- configurable protected fields and replacement markers for secure logging
- structured log-event preparation for public-safe testing and examples
- expanded synthetic education cybersecurity benchmark covering normal activity, suspicious content, assessment misuse, role violations, privacy exposure, institution-content integrity, multi-step cases, and human-review cases
- benchmark validation helpers and unit tests
- Release Readiness GitHub Actions workflow
- automated validation of required documentation, package metadata, benchmark structure, compilation, and unit tests
- expanded Codex maintainer guidance for repository understanding, issue triage, implementation, pull-request review, testing, secure-code review, documentation maintenance, and release validation
- reusable maintainer checklist with explicit human-review boundaries

## Quality Checks

The v0.2.0 release candidate should pass:

- Tests
- Dependency Review
- Release Readiness

## Data Safety

Public examples and benchmark cases use synthetic or public-safe material. The repository must not contain identifiable student data, confidential institution records, restricted examination content, credentials, production secrets, or proprietary third-party material without permission.

## Compatibility

Python requirement remains Python 3.10 or newer.

## Status

This is a development release intended for evaluation, contribution, testing, and continued open-source improvement.

## Maintained By

Optficial Labs Pvt Ltd., Hyderabad, India

Website: https://optficial.ai/
