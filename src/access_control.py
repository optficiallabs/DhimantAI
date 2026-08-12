"""Reference role-based access checks for DhimantAI workflows."""

from __future__ import annotations

ROLE_PERMISSIONS = {
    "student": {"view_learning_content", "submit_attempt", "view_own_progress"},
    "teacher": {"view_learning_content", "view_assigned_progress", "manage_assessment", "review_attempt"},
    "coordinator": {"view_learning_content", "view_cohort_progress", "manage_assessment"},
    "administrator": {"view_learning_content", "view_cohort_progress", "manage_assessment", "manage_users", "manage_content"},
}

SCOPE_RULES = {
    "student": {"self"},
    "teacher": {"self", "assigned_cohort"},
    "coordinator": {"self", "assigned_cohort", "assigned_programme"},
    "administrator": {"self", "assigned_cohort", "assigned_programme", "institution"},
}

HIGH_IMPACT_ACTIONS = {"bulk_export", "manage_users", "manage_content"}


def is_action_allowed(role: str, action: str) -> bool:
    """Return True only when the role explicitly contains the requested permission."""
    return action in ROLE_PERMISSIONS.get(role, set())


def is_scope_allowed(role: str, scope: str) -> bool:
    """Return True only when the requested scope is explicitly allowed for the role."""
    return scope in SCOPE_RULES.get(role, set())


def evaluate_access(role: str, action: str, scope: str = "self") -> dict:
    """Evaluate role, action and scope using fail-closed reference rules.

    High-impact actions that are otherwise permitted are marked for review so that
    production systems can attach additional approval or verification controls.
    """
    if role not in ROLE_PERMISSIONS:
        return {"allowed": False, "decision": "deny", "reason": "unknown_role", "role": role, "action": action, "scope": scope}
    if action not in ROLE_PERMISSIONS[role]:
        return {"allowed": False, "decision": "deny", "reason": "permission_denied", "role": role, "action": action, "scope": scope}
    if not is_scope_allowed(role, scope):
        return {"allowed": False, "decision": "deny", "reason": "scope_denied", "role": role, "action": action, "scope": scope}
    if action in HIGH_IMPACT_ACTIONS:
        return {"allowed": True, "decision": "review", "reason": "high_impact_action_requires_review", "role": role, "action": action, "scope": scope}
    return {"allowed": True, "decision": "allow", "reason": "permission_granted", "role": role, "action": action, "scope": scope}


def authorise(role: str, action: str) -> dict:
    """Backward-compatible action-only authorisation helper.

    This function intentionally preserves the v0.2.x behaviour. New code that
    needs scope evaluation or high-impact review decisions should use
    :func:`evaluate_access`.
    """
    allowed = is_action_allowed(role, action)
    return {
        "allowed": allowed,
        "role": role,
        "action": action,
        "reason": "permission_granted" if allowed else "permission_denied",
    }
