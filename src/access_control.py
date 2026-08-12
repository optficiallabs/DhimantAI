"""Reference role-based access checks for DhimantAI workflows."""

from __future__ import annotations

ROLE_PERMISSIONS = {
    "student": {"view_learning_content", "submit_attempt", "view_own_progress"},
    "teacher": {"view_learning_content", "view_assigned_progress", "manage_assessment", "review_attempt"},
    "coordinator": {"view_learning_content", "view_cohort_progress", "manage_assessment"},
    "administrator": {"view_learning_content", "view_cohort_progress", "manage_assessment", "manage_users", "manage_content"},
}


def is_action_allowed(role: str, action: str) -> bool:
    """Return True only when the role explicitly contains the requested permission."""
    return action in ROLE_PERMISSIONS.get(role, set())


def authorise(role: str, action: str) -> dict:
    allowed = is_action_allowed(role, action)
    return {
        "allowed": allowed,
        "role": role,
        "action": action,
        "reason": "permission_granted" if allowed else "permission_denied",
    }
