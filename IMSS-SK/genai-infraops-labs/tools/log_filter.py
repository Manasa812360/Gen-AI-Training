#!/usr/bin/env python3
"""Filter ERROR and WARN entries from the bundled service logs."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import datetime, time
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
LOG_DIRECTORY = ROOT / "data" / "logs" / "bundle"
INCLUDED_LEVELS = {"ERROR", "WARN"}


@dataclass(frozen=True)
class LogEntry:
    timestamp: datetime
    source: str
    line_number: int
    text: str


def parse_time_argument(value: str) -> time:
    """Parse a clock time accepted by --from or --to."""
    try:
        parsed = time.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"{value!r} is not a valid time; use HH:MM or HH:MM:SS"
        ) from exc

    if parsed.tzinfo is not None:
        raise argparse.ArgumentTypeError("time boundaries must not include a timezone")
    return parsed


def parse_log_line(
    line: str, source: str, line_number: int
) -> LogEntry | None:
    """Return an ERROR or WARN log entry, or None for other lines."""
    text = line.rstrip("\r\n")
    fields = text.split(maxsplit=2)
    if len(fields) < 3 or fields[1] not in INCLUDED_LEVELS:
        return None

    try:
        timestamp = datetime.fromisoformat(fields[0])
    except ValueError:
        return None

    return LogEntry(timestamp, source, line_number, text)


def filter_logs(directory: Path, start: time, end: time) -> list[LogEntry]:
    """Read all files in directory and select entries in the inclusive window."""
    entries: list[LogEntry] = []
    for path in sorted(directory.iterdir()):
        if not path.is_file():
            continue
        with path.open("r", encoding="utf-8") as log_file:
            for line_number, line in enumerate(log_file, start=1):
                entry = parse_log_line(line, path.name, line_number)
                if entry is not None and start <= entry.timestamp.time() <= end:
                    entries.append(entry)

    return sorted(
        entries,
        key=lambda entry: (entry.timestamp, entry.source, entry.line_number),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from",
        dest="start",
        required=True,
        type=parse_time_argument,
        help="start time (HH:MM or HH:MM:SS)",
    )
    parser.add_argument(
        "--to",
        dest="end",
        required=True,
        type=parse_time_argument,
        help="end time (HH:MM or HH:MM:SS)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.start > args.end:
        print("--from must not be later than --to", file=sys.stderr)
        return 2

    try:
        entries = filter_logs(LOG_DIRECTORY, args.start, args.end)
    except OSError as exc:
        print(f"Unable to read logs from {LOG_DIRECTORY}: {exc}", file=sys.stderr)
        return 1

    for entry in entries:
        print(f"{entry.source}: {entry.text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
