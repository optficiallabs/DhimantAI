import unittest

from src.access_control import authorise, is_action_allowed


class TestAccessControl(unittest.TestCase):
    def test_student_can_view_own_progress(self):
        self.assertTrue(is_action_allowed("student", "view_own_progress"))

    def test_student_cannot_manage_users(self):
        self.assertFalse(is_action_allowed("student", "manage_users"))

    def test_admin_can_manage_content(self):
        result = authorise("administrator", "manage_content")
        self.assertTrue(result["allowed"])
        self.assertEqual(result["reason"], "permission_granted")


if __name__ == "__main__":
    unittest.main()
