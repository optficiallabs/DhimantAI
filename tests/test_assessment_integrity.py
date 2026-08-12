import unittest

from src.assessment_integrity import evaluate_request, is_resource_allowed


class TestAssessmentIntegrity(unittest.TestCase):
    def test_guided_practice_allows_hints(self):
        self.assertTrue(is_resource_allowed("guided_practice", "hints"))

    def test_examination_blocks_answer_key(self):
        self.assertFalse(is_resource_allowed("examination", "answer_key"))

    def test_teacher_review_can_access_answer_key(self):
        result = evaluate_request("teacher_review", "answer_key")
        self.assertTrue(result["allowed"])
        self.assertEqual(result["decision"], "allow")


if __name__ == "__main__":
    unittest.main()
