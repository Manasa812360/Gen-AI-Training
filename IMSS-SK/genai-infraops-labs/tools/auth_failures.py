#!/usr/bin/env python3
"""Summarise failed authentication attempts by source IP."""

from __future__ import annotations

import argparse
import csv
import ipaddress
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "logs" / "auth.log"
OUTPUT_PATH = ROOT / "outputs" / "m07" / "auth_summary.csv"
FAILURE_PATTERN = re.compile(
    r"^(?P<timestamp>[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+"
    r".*?\bFailed password for (?P<user>\S+) from (?P<source_ip>\S+)\s"
)
TIMESTAMP_FORMAT = "%b %d %H:%M:%S"
FIELDNAMES = (
    "source_ip",
    "failures",
    "distinct_users",
    "first_seen",
    "last_seen",
)


@dataclass(frozen=True)
class Failure:
    timestamp: datetime
    timestamp_text: str
    user: str
    source_ip: str


@dataclass
class FailureSummary:
    failures: int
    users: set[str]
    first: Failure
    last: Failure


def parse_failure(line: str) -> Failure | None:
    """Parse one failed-password line, ignoring unrelated log entries."""
    match = FAILURE_PATTERN.match(line.rstrip("\r\n"))
    if match is None:
        return None

    try:
        timestamp = datetime.strptime(
            match.group("timestamp"), TIMESTAMP_FORMAT
        )
        source_ip = str(ipaddress.ip_address(match.group("source_ip")))
    except ValueError:
        return None

    return Failure(
        timestamp=timestamp,
        timestamp_text=match.group("timestamp"),
        user=match.group("user"),
        source_ip=source_ip,
    )


def summarise_failures(lines: Iterable[str]) -> list[tuple[str, FailureSummary]]:
    """Aggregate parsed failures by source IP."""
    summaries: dict[str, FailureSummary] = defaultdict()
    for line in lines:
        failure = parse_failure(line)
        if failure is None:
            continue

        summary = summaries.get(failure.source_ip)
        if summary is None:
            summaries[failure.source_ip] = FailureSummary(
                failures=1,
                users={failure.user},
                first=failure,
                last=failure,
            )
            continue

        summary.failures += 1
        summary.users.add(failure.user)
        if failure.timestamp < summary.first.timestamp:
            summary.first = failure
        if failure.timestamp > summary.last.timestamp:
            summary.last = failure

    return sorted(
        summaries.items(),
        key=lambda item: (-item[1].failures, item[0]),
    )


def write_summary(
    summaries: Iterable[tuple[str, FailureSummary]], output_path: Path
) -> None:
    """Write grouped failure counts to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for source_ip, summary in summaries:
            writer.writerow(
                {
                    "source_ip": source_ip,
                    "failures": summary.failures,
                    "distinct_users": len(summary.users),
                    "first_seen": summary.first.timestamp_text,
                    "last_seen": summary.last.timestamp_text,
                }
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=INPUT_PATH,
        help=f"authentication log to parse (default: {INPUT_PATH})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help=f"summary CSV to write (default: {OUTPUT_PATH})",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        with args.input.open("r", encoding="utf-8") as input_file:
            summaries = summarise_failures(input_file)
        write_summary(summaries, args.output)
    except OSError as exc:
        raise SystemExit(f"Unable to process authentication log: {exc}") from exc

    print(f"Wrote {len(summaries)} source IP(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
