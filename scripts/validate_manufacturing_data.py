
"""
Secure AWS Manufacturing Monitoring System
Manufacturing data validation prototype.

Uses synthetic educational data only.
This is not production or industrial control software.
"""

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "manufacturing_records.csv"
REPORT_FILE = PROJECT_ROOT / "results" / "validation_report.json"

REQUIRED_FIELDS = [
    "timestamp",
    "throughput_tpd",
    "residual_oil_pct",
    "moisture_pct",
    "solvent_l_per_tonne",
    "status",
]

# Illustrative validation ranges for this synthetic dataset only.
# These are not recommended real-plant operating limits.
NUMERIC_RANGES = {
    "throughput_tpd": (0, 100),
    "residual_oil_pct": (0, 100),
    "moisture_pct": (0, 100),
    "solvent_l_per_tonne": (0, 500),
}

ALLOWED_STATUSES = {"normal", "warning"}


def validate_record(record, line_number):
    """Return a list of validation findings for one CSV record."""
    findings = []

    for field in REQUIRED_FIELDS:
        if field not in record or not (record.get(field) or "").strip():
            findings.append(f"Missing required field: {field}")

    if findings:
        return findings

    try:
        datetime.strptime(record["timestamp"], "%Y-%m-%d %H:%M")
    except ValueError:
        findings.append("Invalid timestamp format")

    numeric_values = {}

    for field, (minimum, maximum) in NUMERIC_RANGES.items():
        try:
            value = float(record[field])

            if not math.isfinite(value):
                findings.append(f"{field} must be a finite number")
                continue

            numeric_values[field] = value

            if not minimum <= value <= maximum:
                findings.append(
                    f"{field} must be between {minimum} and {maximum}"
                )

        except ValueError:
            findings.append(f"{field} must be numeric")

    if record["status"].strip().lower() not in ALLOWED_STATUSES:
        findings.append("Unrecognized status value")

    # Additional review flags for the synthetic monitoring exercise.
    if numeric_values.get("throughput_tpd") == 0:
        findings.append("REVIEW: Zero throughput")

    if numeric_values.get("residual_oil_pct", 0) > 3:
        findings.append("REVIEW: Elevated residual oil")

    if numeric_values.get("moisture_pct", 0) > 10:
        findings.append("REVIEW: Elevated moisture")

    if numeric_values.get("solvent_l_per_tonne", 0) > 25:
        findings.append("REVIEW: Elevated solvent consumption")

    return findings


def main():
    if not DATA_FILE.exists():
        print(f"ERROR: Data file not found: {DATA_FILE}")
        return

    total_records = 0
    invalid_records = 0
    review_records = 0
    record_results = []

    with DATA_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            print("ERROR: CSV file is empty or has no header.")
            return

        missing_headers = [
            field for field in REQUIRED_FIELDS
            if field not in reader.fieldnames
        ]

        if missing_headers:
            print("ERROR: Missing CSV headers:", ", ".join(missing_headers))
            return

        print("Manufacturing Data Validation Report")
        print("=" * 40)

        for line_number, record in enumerate(reader, start=2):
            total_records += 1
            findings = validate_record(record, line_number)

            errors = [
                finding for finding in findings
                if not finding.startswith("REVIEW:")
            ]
            reviews = [
                finding for finding in findings
                if finding.startswith("REVIEW:")
            ]

            if errors:
                record_status = "INVALID"
            elif reviews:
                record_status = "REVIEW REQUIRED"
            else:
                record_status = "PASS"

            record_results.append({
                "row_number": line_number,
                "status": record_status,
                "findings": findings,
            })

            if errors:
                invalid_records += 1
                print(f"Row {line_number}: INVALID")
                for finding in errors:
                    print(f"  - {finding}")

            if reviews:
                review_records += 1
                print(f"Row {line_number}: REVIEW REQUIRED")
                for finding in reviews:
                    print(f"  - {finding}")

            if not findings:
                print(f"Row {line_number}: PASS")

        print("\nSummary")
        print("-" * 40)
        print(f"Records processed: {total_records}")
        print(f"Invalid records: {invalid_records}")
        print(f"Records requiring review: {review_records}")

        report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "data_file": str(DATA_FILE.relative_to(PROJECT_ROOT)),
            "summary": {
                "records_processed": total_records,
                "invalid_records": invalid_records,
                "records_requiring_review": review_records,
            },
            "records": record_results,
        }

        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

        with REPORT_FILE.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)

        print(f"\nJSON report saved to: {REPORT_FILE.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
