# Changelog

All notable changes to DhimantAI will be documented here.

## [Unreleased]

## [0.3.0] - 2026-08-12

### Added
- working `dhimantai` command-line interface
- role, action, and scope access-control evaluation with fail-closed defaults
- integrated benchmark evaluation across content security, assessment integrity, access control, privacy redaction, and workflow-policy cases
- JSON and Markdown benchmark report generation
- decision matrix and failed-case diagnostics
- benchmark report CI artifact generation
- configurable benchmark quality thresholds for overall and category-level accuracy
- benchmark regression tracking against a reviewed baseline
- detection of newly failing cases, missing baseline cases, decision changes, and category regressions
- dedicated Benchmark Report, Benchmark Thresholds, and Benchmark Regression GitHub Actions workflows
- baseline, regression, reporting, CLI, and threshold test coverage

### Changed
- README now documents the CLI, integrated benchmark execution, and reporting workflow
- benchmark evaluation now records structured traces and decision-count metrics
- access-control logic preserves backward-compatible `authorise()` behaviour while supporting richer `evaluate_access()` decisions
- CI now blocks quality regressions that may still pass absolute thresholds

## [0.2.0] - 2026-08-12

### Added
- structured learning-content security categories, rule identifiers, severity levels, and findings
- expanded assessment-integrity policies for guided practice, revision, examination, and teacher-review modes
- explicit allow/deny reasons and fail-closed handling for unknown modes and resources
- recursive privacy-aware redaction for nested student and institution records
- configurable protected fields and replacement markers for secure logging
- structured log-event preparation
- expanded synthetic education cybersecurity benchmark across eight categories
- benchmark validation helpers and unit tests
- Release Readiness GitHub Actions workflow
- automated validation of required documentation, package metadata, benchmark structure, compilation, and tests
- expanded Codex maintainer workflow and reusable maintainer checklist

### Changed
- strengthened benchmark documentation and public-data safety guidance
- expanded release-readiness documentation
- improved unit-test coverage for content security, assessment integrity, logging, and benchmark validation

## [0.1.0] - 2026-08-12

Initial public open-source development release.

### Added
- expanded project documentation
- contribution, security, conduct, and roadmap files
- content-security reference checks
- role-based access-control reference module
- assessment-integrity rules
- privacy-aware logging helper
- synthetic learning examples
- benchmark documentation and sample cases
- automated unit-test workflow
- dependency-review workflow
- pull-request and issue templates
- Codex maintainer workflow documentation
