# Learning Content Security Checks

DhimantAI includes a small, deterministic reference scanner for public-safe learning material. Its purpose is to demonstrate how suspicious instructions can be identified before content is accepted into a learning workflow.

## Scope

The scanner currently covers these defensive categories:

- instruction manipulation
- assessment integrity
- access control
- confidentiality
- student privacy
- credential safety

Each match produces a structured finding containing a rule identifier, category, severity, matched phrase, and human-readable explanation.

## Result structure

`scan_learning_content(text)` returns:

- `safe`: whether no configured rule matched
- `risk`: highest severity across all findings
- `matches`: matched phrases, retained for backward compatibility
- `categories`: distinct defensive categories detected
- `finding_count`: number of findings
- `findings`: structured per-rule results

## Intended use

This module is designed for:

- synthetic benchmark cases
- unit and regression tests
- demonstration of policy-oriented content validation
- controlled research on education workflow security

It is not intended to be a complete production security system. Real deployments should combine deterministic controls with institution policy, identity and permission checks, secure logging, human review, and appropriate monitoring.

## Data-safety rule

Examples and tests must use synthetic, independently created, properly licensed, or otherwise public-safe material. Do not commit identifiable student data, confidential institution records, restricted examination content, credentials, private keys, authentication tokens, or production secrets.
