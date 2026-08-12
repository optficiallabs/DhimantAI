import unittest

from src.secure_logging import redact_record


class TestSecureLogging(unittest.TestCase):
    def test_redacts_sensitive_fields(self):
        record = {
            "student_name": "Synthetic Student",
            "student_id": "SYN-001",
            "topic": "Algebra",
        }
        result = redact_record(record)
        self.assertEqual(result["student_name"], "[REDACTED]")
        self.assertEqual(result["student_id"], "[REDACTED]")
        self.assertEqual(result["topic"], "Algebra")


if __name__ == "__main__":
    unittest.main()
