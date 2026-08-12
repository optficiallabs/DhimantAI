import json
import tempfile
import unittest
from pathlib import Path

from src.benchmark_reporting import build_report, decision_matrix, failed_cases, render_markdown, write_report_files


class TestBenchmarkReporting(unittest.TestCase):
    def setUp(self):
        self.results = [
            {
                "id": "A",
                "category": "normal",
                "expected_decision": "allow",
                "actual_decision": "allow",
                "correct": True,
                "evaluation": {"module": "access_control", "reason": "permission_granted"},
            },
            {
                "id": "B",
                "category": "assessment",
                "expected_decision": "deny",
                "actual_decision": "review",
                "correct": False,
                "evaluation": {"module": "assessment_integrity", "reason": "manual_review"},
            },
        ]

    def test_decision_matrix(self):
        matrix = decision_matrix(self.results)
        self.assertEqual(matrix["allow"]["allow"], 1)
        self.assertEqual(matrix["deny"]["review"], 1)

    def test_failed_case_diagnostics(self):
        failures = failed_cases(self.results)
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0]["id"], "B")
        self.assertEqual(failures[0]["module"], "assessment_integrity")

    def test_build_and_render_report(self):
        report = build_report(self.results)
        self.assertEqual(report["metrics"]["total"], 2)
        self.assertEqual(report["metrics"]["incorrect"], 1)
        markdown = render_markdown(report)
        self.assertIn("# DhimantAI Benchmark Report", markdown)
        self.assertIn("50.00%", markdown)
        self.assertIn("| B | assessment | deny | review |", markdown)

    def test_write_report_files(self):
        report = build_report(self.results)
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = write_report_files(report, tmpdir, "sample")
            json_path = Path(paths["json"])
            md_path = Path(paths["markdown"])
            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["metrics"]["total"], 2)
            self.assertIn("Failed Cases", md_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
