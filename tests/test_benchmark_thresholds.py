import unittest

from src.benchmark_thresholds import evaluate_thresholds


class TestBenchmarkThresholds(unittest.TestCase):
    def test_passes_when_all_thresholds_met(self):
        metrics = {
            "accuracy": 1.0,
            "categories": {
                "role_violation": {"accuracy": 1.0},
                "assessment_misuse": {"accuracy": 1.0},
            },
        }
        result = evaluate_thresholds(
            metrics,
            minimum_accuracy=0.95,
            category_minimums={"role_violation": 1.0},
        )
        self.assertTrue(result.passed)
        self.assertEqual(result.failures, ())

    def test_fails_overall_accuracy(self):
        metrics = {"accuracy": 0.8, "categories": {}}
        result = evaluate_thresholds(metrics, minimum_accuracy=0.9)
        self.assertFalse(result.passed)
        self.assertTrue(any("overall accuracy" in failure for failure in result.failures))

    def test_fails_category_accuracy(self):
        metrics = {
            "accuracy": 1.0,
            "categories": {"student_data_exposure": {"accuracy": 0.5}},
        }
        result = evaluate_thresholds(
            metrics,
            minimum_accuracy=0.9,
            category_minimums={"student_data_exposure": 1.0},
        )
        self.assertFalse(result.passed)
        self.assertTrue(any("student_data_exposure" in failure for failure in result.failures))

    def test_missing_required_category_fails_closed(self):
        metrics = {"accuracy": 1.0, "categories": {}}
        result = evaluate_thresholds(
            metrics,
            category_minimums={"critical_category": 1.0},
        )
        self.assertFalse(result.passed)
        self.assertTrue(any("missing" in failure for failure in result.failures))


if __name__ == "__main__":
    unittest.main()
