#!/usr/bin/env python3
"""Summarise an nginx combined access log by hour and HTTP status."""

from __future__ import annotations

import argparse
import csv
import ipaddress
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence


LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+) (?P<protocol>HTTP/\d+(?:\.\d+)?)" '
    r'(?P<status>\d{3}) (?:\d+|-) '
    r'"(?:[^"\\]|\\.)*" "(?:[^"\\]|\\.)*"$'
)
LOG_TIME_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


@dataclass(frozen=True)
class LogEntry:
    """Fields extracted from one valid nginx access log line."""

    ip: str
    time: datetime
    method: str
    path: str
    status: int


def parse_line(line: str) -> LogEntry | None:
    """Parse a combined-format line, returning ``None`` when it is malformed."""
    match = LOG_PATTERN.fullmatch(line.strip())
    if match is None:
        return None

    try:
        ipaddress.ip_address(match.group("ip"))
        timestamp = datetime.strptime(match.group("time"), LOG_TIME_FORMAT)
        status = int(match.group("status"))
    except ValueError:
        return None

    if not 100 <= status <= 599:
        return None

    return LogEntry(
        ip=match.group("ip"),
        time=timestamp,
        method=match.group("method"),
        path=match.group("path"),
        status=status,
    )


def count_requests(lines: Iterable[str]) -> tuple[Counter[tuple[datetime, int]], int]:
    """Count valid requests per hour/status and report malformed line count."""
    counts: Counter[tuple[datetime, int]] = Counter()
    malformed = 0

    for line in lines:
        entry = parse_line(line)
        if entry is None:
            malformed += 1
            continue

        hour = entry.time.replace(minute=0, second=0, microsecond=0)
        counts[(hour, entry.status)] += 1

    return counts, malformed


def write_csv(
    counts: Counter[tuple[datetime, int]],
    output_path: Path,
) -> None:
    """Write hourly status counts to a CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(("hour", "status", "count"))
        for (hour, status), count in sorted(counts.items()):
            writer.writerow((hour.isoformat(), status, count))


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Count nginx requests by hour and HTTP status code."
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="path to an nginx combined access log",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="path for the generated CSV",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line log summariser."""
    args = build_parser().parse_args(argv)

    try:
        with args.input.open("r", encoding="utf-8") as input_file:
            counts, malformed = count_requests(input_file)
        write_csv(counts, args.output)
    except OSError as exc:
        raise SystemExit(f"Unable to process log: {exc}") from exc

    print(f"Skipped {malformed} malformed line(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
