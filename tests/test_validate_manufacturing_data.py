
import unittest

from scripts.validate_manufacturing_data import validate_record


class TestManufacturingDataValidation(unittest.TestCase):

    def setUp(self):
        self.valid_record = {
            "timestamp": "2026-10-20 08:00",
            "throughput_tpd": "25",
            "residual_oil_pct": "2.4",
            "moisture_pct": "8.5",
            "solvent_l_per_tonne": "18",
            "status": "normal",
        }

    def test_valid_record_has_no_findings(self):
        findings = validate_record(self.valid_record.copy(), 2)
        self.assertEqual(findings, [])

    def test_invalid_timestamp_is_detected(self):
        record = self.valid_record.copy()
        record["timestamp"] = "invalid-date"

        findings = validate_record(record, 2)

        self.assertIn("Invalid timestamp format", findings)

    def test_non_numeric_throughput_is_detected(self):
        record = self.valid_record.copy()
        record["throughput_tpd"] = "abc"

        findings = validate_record(record, 2)

        self.assertIn("throughput_tpd must be numeric", findings)

    def test_missing_field_is_detected(self):
        record = self.valid_record.copy()
        del record["moisture_pct"]

        findings = validate_record(record, 2)

        self.assertIn("Missing required field: moisture_pct", findings)

    def test_zero_throughput_requires_review(self):
        record = self.valid_record.copy()
        record["throughput_tpd"] = "0"

        findings = validate_record(record, 2)

        self.assertIn("REVIEW: Zero throughput", findings)

    def test_elevated_residual_oil_requires_review(self):
        record = self.valid_record.copy()
        record["residual_oil_pct"] = "3.8"

        findings = validate_record(record, 2)

        self.assertIn("REVIEW: Elevated residual oil", findings)

    def test_unrecognized_status_is_detected(self):
        record = self.valid_record.copy()
        record["status"] = "unknown"

        findings = validate_record(record, 2)

        self.assertIn("Unrecognized status value", findings)

    def test_non_finite_numeric_values_are_rejected(self):
        for value in ("NaN", "inf", "-inf"):
            with self.subTest(value=value):
                record = self.valid_record.copy()
                record["throughput_tpd"] = value

                findings = validate_record(record, 2)

                self.assertIn(
                    "throughput_tpd must be a finite number",
                    findings,
                )


if __name__ == "__main__":
    unittest.main()

