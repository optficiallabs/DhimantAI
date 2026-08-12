import unittest

from src.secure_logging import prepare_log_event, redact_record


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

    def test_redacts_nested_records_and_lists(self):
        record = {
            "course": "Mathematics",
            "student": {
                "student_email": "student@example.invalid",
                "progress": 80,
            },
            "participants": [
                {"student_name": "Learner A", "role": "student"},
                {"student_name": "Learner B", "role": "student"},
            ],
        }
        result = redact_record(record)
        self.assertEqual(result["student"]["student_email"], "[REDACTED]")
        self.assertEqual(result["student"]["progress"], 80)
        self.assertEqual(result["participants"][0]["student_name"], "[REDACTED]")

    def test_custom_sensitive_fields_and_replacement(self):
        record = {"internal_class_code": "CLS-42", "topic": "Physics"}
        result = redact_record(
            record,
            sensitive_fields={"internal_class_code"},
            replacement="***",
        )
        self.assertEqual(result["internal_class_code"], "***")
        self.assertEqual(result["topic"], "Physics")

    def test_field_matching_is_case_insensitive(self):
        result = redact_record({"Student_Email": "student@example.invalid"})
        self.assertEqual(result["Student_Email"], "[REDACTED]")

    def test_original_record_is_not_modified(self):
        record = {"student_name": "Synthetic Student"}
        redact_record(record)
        self.assertEqual(record["student_name"], "Synthetic Student")

    def test_prepare_log_event_returns_redacted_data(self):
        event = prepare_log_event(
            "learning_session",
            {"student_id": "SYN-123", "action": "opened_lesson"},
        )
        self.assertEqual(event["event_type"], "learning_session")
        self.assertEqual(event["data"]["student_id"], "[REDACTED]")
        self.assertEqual(event["data"]["action"], "opened_lesson")


if __name__ == "__main__":
    unittest.main()
