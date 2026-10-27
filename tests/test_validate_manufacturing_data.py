import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.validate_manufacturing_data as validator
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
        self.assertEqual(
            validate_record(self.valid_record.copy(), 2), []
        )

    def test_invalid_timestamp_is_detected(self):
        record = self.valid_record.copy()
        record["timestamp"] = "invalid-date"
        self.assertIn(
            "Invalid timestamp format", validate_record(record, 2)
        )

    def test_non_numeric_throughput_is_detected(self):
        record = self.valid_record.copy()
        record["throughput_tpd"] = "abc"
        self.assertIn(
            "throughput_tpd must be numeric",
            validate_record(record, 2),
        )

    def test_missing_field_is_detected(self):
        record = self.valid_record.copy()
        del record["moisture_pct"]
        self.assertIn(
            "Missing required field: moisture_pct",
            validate_record(record, 2),
        )

    def test_zero_throughput_requires_review(self):
        record = self.valid_record.copy()
        record["throughput_tpd"] = "0"
        self.assertIn(
            "REVIEW: Zero throughput", validate_record(record, 2)
        )

    def test_elevated_residual_oil_requires_review(self):
        record = self.valid_record.copy()
        record["residual_oil_pct"] = "3.8"
        self.assertIn(
            "REVIEW: Elevated residual oil",
            validate_record(record, 2),
        )

    def test_unrecognized_status_is_detected(self):
        record = self.valid_record.copy()
        record["status"] = "unknown"
        self.assertIn(
            "Unrecognized status value", validate_record(record, 2)
        )

    def test_non_finite_numeric_values_are_rejected(self):
        for value in ("NaN", "inf", "-inf"):
            with self.subTest(value=value):
                record = self.valid_record.copy()
                record["throughput_tpd"] = value
                self.assertIn(
                    "throughput_tpd must be a finite number",
                    validate_record(record, 2),
                )


class TestJsonValidationReport(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.root = Path(self.temp_dir.name)
        self.data_path = self.root / "data" / "manufacturing_records.csv"
        self.report_path = (
            self.root / "results" / "validation_report.json"
        )

        self.data_path.parent.mkdir(parents=True)

        records = [
            {
                "timestamp": "2026-10-20 08:00",
                "throughput_tpd": "25",
                "residual_oil_pct": "2.4",
                "moisture_pct": "8.5",
                "solvent_l_per_tonne": "18",
                "status": "normal",
            },
            {
                "timestamp": "2026-10-20 09:00",
                "throughput_tpd": "25",
                "residual_oil_pct": "3.8",
                "moisture_pct": "8.5",
                "solvent_l_per_tonne": "18",
                "status": "warning",
            },
        ]

        with self.data_path.open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file, fieldnames=validator.REQUIRED_FIELDS
            )
            writer.writeheader()
            writer.writerows(records)

        patches = [
            patch.object(validator, "PROJECT_ROOT", self.root),
            patch.object(validator, "DATA_FILE", self.data_path),
            patch.object(validator, "REPORT_FILE", self.report_path),
        ]

        for item in patches:
            item.start()
            self.addCleanup(item.stop)

    def run_validation(self):
        validator.main()

        with self.report_path.open(
            "r", encoding="utf-8"
        ) as file:
            return json.load(file)

    def test_json_report_is_generated_with_expected_summary(self):
        report = self.run_validation()

        self.assertTrue(self.report_path.exists())
        self.assertIn("generated_at", report)
        self.assertEqual(report["summary"]["records_processed"], 2)
        self.assertEqual(report["summary"]["invalid_records"], 0)
        self.assertEqual(
            report["summary"]["records_requiring_review"], 1
        )

    def test_json_report_records_have_required_fields(self):
        report = self.run_validation()

        self.assertEqual(len(report["records"]), 2)

        for record in report["records"]:
            self.assertIn("row_number", record)
            self.assertIn("status", record)
            self.assertIn("findings", record)

        self.assertEqual(report["records"][0]["status"], "PASS")
        self.assertEqual(
            report["records"][1]["status"], "REVIEW REQUIRED"
        )


if __name__ == "__main__":
    unittest.main()
