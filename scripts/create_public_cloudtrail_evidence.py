import json
from pathlib import Path

source = Path("evidence/cloudtrail/s3_object_events.json")
destination = Path("evidence/public/cloudtrail_s3_object_events.json")

if not source.exists():
    raise FileNotFoundError(f"Evidence file not found: {source}")

with source.open("r", encoding="utf-8") as file:
    events = json.load(file)

public_events = []

for event in events:
    event_name = event.get("event_name")

    if event_name == "GetObject":
        resource = "manufacturing_records.csv"
    elif event_name == "PutObject":
        resource = "reports/validation_report.json"
    else:
        resource = "other S3 object"

    public_events.append({
        "event_time_utc": event.get("event_time"),
        "event_name": event_name,
        "region": event.get("region"),
        "resource": resource,
        "identity_type": event.get("identity_type"),
        "role_name": event.get("role_name"),
        "result": (
            "No error code or error message recorded"
            if not event.get("error_code")
            and not event.get("error_message")
            else "Error recorded"
        )
    })

destination.parent.mkdir(parents=True, exist_ok=True)

with destination.open("w", encoding="utf-8") as file:
    json.dump(public_events, file, indent=2)

print(f"Public evidence saved to: {destination}")
print(f"Events included: {len(public_events)}")
print(json.dumps(public_events, indent=2))
