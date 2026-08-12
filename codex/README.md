# Codex Maintainer Workflow for DhimantAI

This directory documents a review-first workflow for using Codex in authorised DhimantAI software-development tasks.

Codex can assist maintainers with repository understanding, code changes, tests, pull-request review, documentation and release preparation. Final decisions about code, security, assessment integrity, privacy and releases remain with human maintainers.

## 1. Repository understanding

Use Codex to inspect the repository before making changes. A useful starting task is to ask it to explain:

- the purpose of each top-level directory
- the security-sensitive modules in `src/`
- the current test coverage
- the benchmark structure
- the CI workflows
- the contribution and security policies

The maintainer should verify the summary against the repository before acting on it.

## 2. Issue triage

For an issue, ask Codex to:

1. restate the requested behaviour;
2. identify the files likely to change;
3. identify security, privacy or assessment-integrity implications;
4. propose acceptance criteria;
5. suggest tests before implementation.

Do not treat a generated implementation plan as approval to change policy-sensitive behaviour.

## 3. Implementing changes

Prefer small, reviewable changes on a dedicated branch. The expected workflow is:

1. read the issue and related documentation;
2. inspect existing code and tests;
3. propose the smallest suitable change;
4. implement the change;
5. add or update tests;
6. run the relevant test suite;
7. review the diff manually;
8. open a pull request;
9. wait for required GitHub Actions checks;
10. merge only after maintainer review.

## 4. Pull-request review

Codex may help review a pull request by checking for:

- unintended behaviour changes
- missing validation
- weak error handling
- insufficient tests
- inconsistent documentation
- permission or role-boundary regressions
- student-data exposure
- unsafe logging
- assessment-integrity regressions
- benchmark-format inconsistencies

Security findings should be validated by a maintainer before being reported as confirmed vulnerabilities.

## 5. Test preparation

When preparing tests, ask for cases that cover:

- expected successful behaviour
- denied or blocked behaviour
- unknown or malformed inputs
- boundary conditions
- nested data structures where relevant
- permission failures
- privacy-preserving output
- regression cases for previously fixed issues

Tests should use synthetic or otherwise public-safe educational data.

## 6. Secure-code review

For security-sensitive changes, focus review on defensive properties such as:

- least-privilege access
- fail-closed behaviour for unknown permissions
- protection of student and institution information
- redaction before logging
- validation of content and benchmark records
- explicit assessment-mode boundaries
- dependency changes
- reproducible security decisions

Do not use this repository workflow to target systems without authorisation or to process material that is not suitable for the configured development environment.

## 7. Documentation maintenance

After a code change, check whether the following require updates:

- `README.md`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `ROADMAP.md`
- `CHANGELOG.md`
- files under `docs/`
- benchmark documentation
- release notes

Documentation should describe the implemented behaviour and limitations rather than planned behaviour as if it were already complete.

## 8. Release validation

Before a versioned release, maintainers should run:

```bash
python -m unittest discover -s tests -p "test_*.py"
python scripts/check_release_readiness.py
```

The repository also includes GitHub Actions for unit tests, dependency review and release readiness. A release should not proceed when required checks are failing or when unresolved high-impact privacy, security or assessment-integrity concerns remain.

## 9. Human review boundaries

Human approval is required for decisions involving:

- changes to access-control policy
- examination or assessment-integrity rules
- handling of student or institution information
- security findings that may require responsible disclosure
- dependency-risk exceptions
- benchmark publication decisions
- release approval

Codex should be used as an engineering assistant, not as the final authority for these decisions.

## 10. Data-safety rules

Do not provide Codex with real student information, confidential institution records, restricted examination content, passwords, private keys, authentication tokens, production secrets, or proprietary third-party material unless the environment and permissions explicitly permit that use.

For this public repository, examples and tests should remain synthetic, independently created, properly licensed, or otherwise public-safe.
