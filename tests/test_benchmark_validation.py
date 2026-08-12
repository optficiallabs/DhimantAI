import unittest

from src.benchmark_validation import summarise_cases, validate_benchmark_case


class TestBenchmarkValidation(unittest.TestCase):
    def test_valid_case_has_no_errors(self):
        case = {
            "id": "EDU-001",
            "category": "normal_learning",
            "scenario": "Synthetic guided-practice request.",
            "expected_decision": "allow",
            "expected_reason": "within normal permissions",
            "human_review": False,
        }
        self.assertEqual(validate_benchmark_case(case), [])

    def test_missing_fields_are_reported(self):
        errors = validate_benchmark_case({"id": "EDU-002"})
        self.assertTrue(any("missing fields" in error for error in errors))

    def test_invalid_decision_is_reported(self):
        case = {
            "id": "EDU-003",
            "category": "normal_learning",
            "scenario": "Synthetic case",
            "expected_decision": "unknown",
            "expected_reason": "test",
            "human_review": False,
        }
        errors = validate_benchmark_case(case)
        self.assertIn("unsupported expected_decision: unknown", errors)

    def test_summary_counts_categories_and_reviews(self):
        cases = [
            {"category": "normal_learning", "human_review": False},
            {"category": "normal_learning", "human_review": False},
            {"category": "human_review", "human_review": True},
        ]
        result = summarise_cases(cases)
        self.assertEqual(result["total_cases"], 3)
        self.assertEqual(result["categories"]["normal_learning"], 2)
        self.assertEqual(result["human_review_cases"], 1)


if __name__ == "__main__":
    unittest.main()
