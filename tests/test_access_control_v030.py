import unittest

from src.access_control import evaluate_access, is_scope_allowed


class TestAccessControlV030(unittest.TestCase):
    def test_student_self_scope_allowed(self):
        result = evaluate_access("student", "view_own_progress", "self")
        self.assertTrue(result["allowed"])
        self.assertEqual(result["decision"], "allow")

    def test_student_cross_scope_denied(self):
        result = evaluate_access("student", "view_own_progress", "assigned_cohort")
        self.assertFalse(result["allowed"])
        self.assertEqual(result["reason"], "scope_denied")

    def test_unknown_role_fails_closed(self):
        result = evaluate_access("unknown", "view_learning_content")
        self.assertFalse(result["allowed"])
        self.assertEqual(result["reason"], "unknown_role")

    def test_admin_manage_users_requires_review(self):
        result = evaluate_access("administrator", "manage_users", "institution")
        self.assertTrue(result["allowed"])
        self.assertEqual(result["decision"], "review")

    def test_scope_helper(self):
        self.assertTrue(is_scope_allowed("teacher", "assigned_cohort"))
        self.assertFalse(is_scope_allowed("teacher", "institution"))


if __name__ == "__main__":
    unittest.main()
