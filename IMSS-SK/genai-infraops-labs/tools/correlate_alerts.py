#!/usr/bin/env python3
"""Correlate alerts by business service and five-minute time window.

Usage:
    python tools/correlate_alerts.py
    python tools/correlate_alerts.py --alerts <file> --inventory <file> --out <file>
"""

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


WINDOW = timedelta(minutes=5)
ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--alerts",
        type=Path,
        default=ROOT / "data/alerts/alerts_stream.json",
        help="alert stream JSON file",
    )
    parser.add_argument(
        "--inventory",
        type=Path,
        default=ROOT / "data/cmdb/ci_inventory.csv",
        help="CMDB inventory CSV file",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "outputs/m06/alert_groups.json",
        help="output JSON file",
    )
    return parser.parse_args()


def load_business_services(inventory_path: Path) -> dict[str, str]:
    with inventory_path.open(newline="", encoding="utf-8") as inventory_file:
        reader = csv.DictReader(inventory_file)
        required = {"ci_name", "business_service"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(
                f"{inventory_path} must contain columns: {', '.join(sorted(required))}"
            )

        services: dict[str, str] = {}
        for row_number, row in enumerate(reader, start=2):
            ci_name = (row.get("ci_name") or "").strip()
            business_service = (row.get("business_service") or "").strip()
            if not ci_name or not business_service:
                raise ValueError(
                    f"{inventory_path}:{row_number} has an empty ci_name or business_service"
                )
            if ci_name in services:
                raise ValueError(
                    f"{inventory_path}:{row_number} duplicates CI {ci_name!r}"
                )
            services[ci_name] = business_service

    return services


def load_alerts(alerts_path: Path) -> list[dict[str, Any]]:
    with alerts_path.open(encoding="utf-8") as alerts_file:
        document = json.load(alerts_file)

    alerts = document.get("alerts") if isinstance(document, dict) else None
    if not isinstance(alerts, list):
        raise ValueError(f"{alerts_path} must contain an 'alerts' array")

    required = {"id", "fired_at", "instance"}
    validated: list[dict[str, Any]] = []
    alert_ids: set[str] = set()
    for index, alert in enumerate(alerts):
        if not isinstance(alert, dict):
            raise ValueError(f"{alerts_path} alert {index + 1} is not an object")
        missing = required - alert.keys()
        if missing:
            raise ValueError(
                f"{alerts_path} alert {index + 1} is missing: "
                f"{', '.join(sorted(missing))}"
            )
        alert_id = str(alert["id"])
        if alert_id in alert_ids:
            raise ValueError(f"{alerts_path} duplicates alert ID {alert_id!r}")
        try:
            fired_at = datetime.fromisoformat(str(alert["fired_at"]))
        except ValueError as exc:
            raise ValueError(
                f"{alerts_path} alert {alert_id!r} has invalid fired_at "
                f"{alert['fired_at']!r}"
            ) from exc
        if fired_at.tzinfo is None:
            raise ValueError(
                f"{alerts_path} alert {alert_id!r} fired_at must include a timezone"
            )

        alert_ids.add(alert_id)
        validated.append({**alert, "id": alert_id, "_fired_at": fired_at})

    return validated


def select_root_candidate(alerts: list[dict[str, Any]]) -> str:
    critical = [alert for alert in alerts if alert.get("severity") == "critical"]
    return min(critical or alerts, key=lambda alert: alert["_fired_at"])["id"]


def correlate_alerts(
    alerts: list[dict[str, Any]],
    business_services: dict[str, str],
) -> list[dict[str, Any]]:
    by_service: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for alert in alerts:
        instance = str(alert["instance"])
        if instance not in business_services:
            raise ValueError(
                f"alert {alert['id']!r} references CI {instance!r}, "
                "which is missing from the inventory"
            )
        by_service[business_services[instance]].append(alert)

    candidate_groups: list[tuple[datetime, str, list[dict[str, Any]]]] = []
    for business_service, service_alerts in by_service.items():
        service_alerts.sort(key=lambda alert: (alert["_fired_at"], alert["id"]))
        current: list[dict[str, Any]] = []
        for alert in service_alerts:
            if current and alert["_fired_at"] - current[0]["_fired_at"] > WINDOW:
                candidate_groups.append(
                    (current[0]["_fired_at"], business_service, current)
                )
                current = []
            current.append(alert)
        if current:
            candidate_groups.append(
                (current[0]["_fired_at"], business_service, current)
            )

    candidate_groups.sort(key=lambda item: (item[0], item[1]))
    output: list[dict[str, Any]] = []
    for number, (_, business_service, group_alerts) in enumerate(
        candidate_groups, start=1
    ):
        root_candidate = select_root_candidate(group_alerts)
        output.append(
            {
                "group_id": f"GRP-{number:04d}",
                "business_service": business_service,
                "root_candidate": root_candidate,
                "child_alert_ids": [
                    alert["id"]
                    for alert in group_alerts
                    if alert["id"] != root_candidate
                ],
                "count": len(group_alerts),
            }
        )

    return output


def print_summary(groups: list[dict[str, Any]]) -> None:
    headers = ("group_id", "business_service", "root_candidate", "count")
    rows = [
        (
            group["group_id"],
            group["business_service"],
            group["root_candidate"],
            str(group["count"]),
        )
        for group in groups
    ]
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in rows))
        for index in range(len(headers))
    ]

    def format_row(row: tuple[str, ...]) -> str:
        return " | ".join(value.ljust(widths[index]) for index, value in enumerate(row))

    separator = "-+-".join("-" * width for width in widths)
    print(format_row(headers))
    print(separator)
    for row in rows:
        print(format_row(row))
    print(f"\nCorrelated {sum(group['count'] for group in groups)} alerts into {len(groups)} groups.")


def main() -> None:
    args = parse_args()
    business_services = load_business_services(args.inventory)
    alerts = load_alerts(args.alerts)
    groups = correlate_alerts(alerts, business_services)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as output_file:
        json.dump(groups, output_file, indent=2)
        output_file.write("\n")

    print_summary(groups)
    print(f"Saved: {args.out}")


if __name__ == "__main__":
    main()
