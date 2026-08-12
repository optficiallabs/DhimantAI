import tempfile
import unittest
from pathlib import Path

from src.benchmark_runner import calculate_metrics, load_jsonl, run_benchmark


class TestBenchmarkRunner(unittest.TestCase):
    def test_load_jsonl(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cases.jsonl"
            path.write_text('{"id":"A","category":"normal","expected_decision":"allow"}\n', encoding="utf-8")
            cases = load_jsonl(path)
            self.assertEqual(len(cases), 1)
            self.assertEqual(cases[0]["id"], "A")

    def test_run_and_metrics(self):
        cases = [
            {"id": "A", "category": "normal", "expected_decision": "allow"},
            {"id": "B", "category": "normal", "expected_decision": "deny"},
            {"id": "C", "category": "review", "expected_decision": "review"},
        ]
        decisions = {"A": "allow", "B": "allow", "C": "review"}
        results = run_benchmark(cases, lambda case: decisions[case["id"]])
        metrics = calculate_metrics(results)
        self.assertEqual(metrics["total"], 3)
        self.assertEqual(metrics["correct"], 2)
        self.assertAlmostEqual(metrics["accuracy"], 2 / 3)
        self.assertEqual(metrics["categories"]["normal"]["correct"], 1)

    def test_invalid_json_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.jsonl"
            path.write_text('{bad json}\n', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_jsonl(path)


if __name__ == "__main__":
    unittest.main()
