import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from src.cli import main


class TestCLI(unittest.TestCase):
    def _run(self, argv):
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = main(argv)
        return code, json.loads(stream.getvalue())

    def test_check_access(self):
        code, payload = self._run(["check-access", "student", "view_own_progress"])
        self.assertEqual(code, 0)
        self.assertEqual(payload["decision"], "allow")

    def test_validate_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "content.txt"
            path.write_text("Explain fractions using a simple example.", encoding="utf-8")
            code, payload = self._run(["validate-content", str(path)])
            self.assertEqual(code, 0)
            self.assertTrue(payload["safe"])

    def test_run_benchmark(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cases.jsonl"
            path.write_text('{"id":"A","category":"normal","expected_decision":"allow"}\n', encoding="utf-8")
            code, payload = self._run(["run-benchmark", str(path)])
            self.assertEqual(code, 0)
            self.assertEqual(payload["accuracy"], 1.0)

    def test_generate_benchmark_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            case_path = Path(tmpdir) / "cases.jsonl"
            output_dir = Path(tmpdir) / "report"
            case_path.write_text(
                '{"id":"A","category":"normal","expected_decision":"allow","evaluator":"workflow_policy","input":{"decision":"allow","reason":"synthetic_test"}}\n',
                encoding="utf-8",
            )
            code, payload = self._run([
                "generate-benchmark-report",
                str(case_path),
                "--output-dir",
                str(output_dir),
                "--stem",
                "ci-report",
            ])
            self.assertEqual(code, 0)
            self.assertEqual(payload["metrics"]["accuracy"], 1.0)
            self.assertTrue(Path(payload["paths"]["json"]).exists())
            self.assertTrue(Path(payload["paths"]["markdown"]).exists())


if __name__ == "__main__":
    unittest.main()
