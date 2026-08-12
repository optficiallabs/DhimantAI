# Release Readiness

DhimantAI releases should pass both automated checks and a short maintainer review before a version is published.

## Automated checks

The `Release Readiness` GitHub Actions workflow runs on pull requests to `main`, version-tag pushes, and manual dispatch. It performs:

- Python source compilation
- the full unit-test suite
- required-file checks
- package-metadata checks from `pyproject.toml`
- expanded benchmark presence and JSONL structure checks
- duplicate benchmark-ID detection

Dependency changes are separately checked by the `Dependency Review` workflow on pull requests.

## Maintainer review

Before a release, maintainers should also confirm:

- no real student or confidential institution data is present
- no credentials, authentication tokens, production secrets, or restricted assessment material are included
- security-sensitive changes have been reviewed
- assessment-integrity rules behave as intended
- role and permission changes are documented
- benchmark examples remain synthetic or public-safe
- dependency changes have passed review
- README and technical documentation match the current code
- `CHANGELOG.md` and release notes describe important changes and limitations
- the release tag matches the intended package version

## Hold conditions

A release should be held when:

- automated tests fail
- release-readiness validation fails
- dependency review reports an unresolved unacceptable risk
- a high-impact privacy, security, or assessment-integrity issue remains unresolved
- public artifacts contain information that should not be released

## Local check

Maintainers can run:

```bash
python -m unittest discover -s tests -p "test_*.py"
python scripts/check_release_readiness.py
```

Passing these checks does not replace human review; it provides a consistent minimum release gate.
