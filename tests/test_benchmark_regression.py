import unittest

from src.benchmark_regression import compare_to_baseline


class TestBenchmarkRegression(unittest.TestCase):
    def setUp(self):
        self.baseline = {
            "accuracy": 1.0,
            "categories": {"normal": {"accuracy": 1.0}},
            "cases": {
                "A": {"category": "normal", "decision": "allow", "correct": True},
                "B": {"category": "normal", "decision": "deny", "correct": True},
            },
        }

    def test_no_regression_passes(self):
        results = [
            {"id": "A", "category": "normal", "actual_decision": "allow", "correct": True},
            {"id": "B", "category": "normal", "actual_decision": "deny", "correct": True},
        ]
        metrics = {"accuracy": 1.0, "categories": {"normal": {"accuracy": 1.0}}}
        comparison = compare_to_baseline(results, metrics, self.baseline)
        self.assertTrue(comparison.passed)
        self.assertEqual(comparison.newly_failing_cases, [])

    def test_new_failure_is_regression(self):
        results = [
            {"id": "A", "category": "normal", "actual_decision": "allow", "correct": True},
            {"id": "B", "category": "normal", "actual_decision": "allow", "correct": False},
        ]
        metrics = {"accuracy": 0.5, "categories": {"normal": {"accuracy": 0.5}}}
        comparison = compare_to_baseline(results, metrics, self.baseline)
        self.assertFalse(comparison.passed)
        self.assertIn("B", comparison.newly_failing_cases)
        self.assertEqual(comparison.changed_decisions[0]["id"], "B")

    def test_missing_baseline_case_fails_closed(self):
        results = [{"id": "A", "category": "normal", "actual_decision": "allow", "correct": True}]
        metrics = {"accuracy": 1.0, "categories": {"normal": {"accuracy": 1.0}}}
        comparison = compare_to_baseline(results, metrics, self.baseline)
        self.assertFalse(comparison.passed)
        self.assertEqual(comparison.missing_baseline_cases, ["B"])

    def test_new_passing_case_is_reported_but_allowed(self):
        results = [
            {"id": "A", "category": "normal", "actual_decision": "allow", "correct": True},
            {"id": "B", "category": "normal", "actual_decision": "deny", "correct": True},
            {"id": "C", "category": "normal", "actual_decision": "allow", "correct": True},
        ]
        metrics = {"accuracy": 1.0, "categories": {"normal": {"accuracy": 1.0}}}
        comparison = compare_to_baseline(results, metrics, self.baseline)
        self.assertTrue(comparison.passed)
        self.assertEqual(comparison.added_cases, ["C"])


if __name__ == "__main__":
    unittest.main()
