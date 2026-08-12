import unittest

from src.assessment_integrity import evaluate_request, is_resource_allowed


class TestAssessmentIntegrity(unittest.TestCase):
    def test_guided_practice_allows_hints(self):
        self.assertTrue(is_resource_allowed("guided_practice", "hints"))

    def test_guided_practice_blocks_answer_key(self):
        result = evaluate_request("guided_practice", "answer_key")
        self.assertFalse(result["allowed"])
        self.assertEqual(result["decision"], "deny")

    def test_revision_allows_worked_examples(self):
        result = evaluate_request("revision", "worked_example")
        self.assertTrue(result["allowed"])
        self.assertEqual(result["decision"], "allow")

    def test_examination_blocks_hints(self):
        result = evaluate_request("examination", "hints")
        self.assertFalse(result["allowed"])
        self.assertIn("restricted", result["reason"].lower())

    def test_examination_blocks_answer_key(self):
        self.assertFalse(is_resource_allowed("examination", "answer_key"))

    def test_teacher_review_can_access_answer_key(self):
        result = evaluate_request("teacher_review", "answer_key")
        self.assertTrue(result["allowed"])
        self.assertEqual(result["decision"], "allow")

    def test_unknown_mode_fails_closed(self):
        result = evaluate_request("unknown_mode", "hints")
        self.assertFalse(result["allowed"])
        self.assertFalse(result["mode_known"])
        self.assertEqual(result["decision"], "deny")

    def test_unknown_resource_fails_closed(self):
        result = evaluate_request("guided_practice", "unlisted_resource")
        self.assertFalse(result["allowed"])
        self.assertFalse(result["resource_known"])
        self.assertEqual(result["decision"], "deny")


if __name__ == "__main__":
    unittest.main()
