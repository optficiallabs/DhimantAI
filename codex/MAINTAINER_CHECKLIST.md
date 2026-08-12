# Codex Maintainer Checklist

Use this checklist when Codex assists with a DhimantAI change.

## Before editing

- [ ] Read the issue and relevant documentation.
- [ ] Confirm the task is authorised and within repository scope.
- [ ] Identify privacy, security and assessment-integrity implications.
- [ ] Confirm examples and fixtures are synthetic or public-safe.

## During implementation

- [ ] Keep the change focused and reviewable.
- [ ] Preserve least-privilege and fail-closed behaviour where applicable.
- [ ] Add or update tests.
- [ ] Avoid logging identifiable student or confidential institution information.
- [ ] Review dependency changes separately.

## Before opening a pull request

- [ ] Run the unit tests.
- [ ] Review the complete diff manually.
- [ ] Update documentation where behaviour changed.
- [ ] Confirm benchmark records remain valid and public-safe.
- [ ] Include the related issue in the pull-request description.

## Before merge

- [ ] Tests pass.
- [ ] Dependency Review passes.
- [ ] Release Readiness passes when applicable.
- [ ] Human maintainer review is complete.
- [ ] Any security-sensitive finding has been independently validated.

## Before release

- [ ] Run `python scripts/check_release_readiness.py`.
- [ ] Confirm the changelog and release notes match the code.
- [ ] Confirm no sensitive data or secrets are present.
- [ ] Confirm unresolved high-impact security or privacy issues do not remain.
- [ ] Obtain final maintainer approval.
