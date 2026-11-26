"""Tests for the nginx access log parser."""

from datetime import datetime, timedelta, timezone
from pathlib import Path

from log_parser import count_requests, parse_line, write_csv


VALID_LINE = (
    '10.40.3.161 - - [09/Nov/2026:08:00:00 +0530] '
    '"GET /login HTTP/1.1" 200 6261 "-" "Mozilla/5.0"'
)


def test_parse_line_extracts_expected_fields() -> None:
    """A valid combined log line should yield all requested fields."""
    entry = parse_line(VALID_LINE)

    assert entry is not None
    assert entry.ip == "10.40.3.161"
    assert entry.time == datetime(
        2026, 11, 9, 8, tzinfo=timezone(timedelta(hours=5, minutes=30))
    )
    assert entry.method == "GET"
    assert entry.path == "/login"
    assert entry.status == 200


def test_count_requests_skips_malformed_lines() -> None:
    """Malformed rows should be counted without entering the summary."""
    counts, malformed = count_requests([VALID_LINE, "not an nginx line"])

    assert malformed == 1
    assert list(counts.values()) == [1]
    assert next(iter(counts))[1] == 200


def test_write_csv_groups_requests_by_hour_and_status(tmp_path: Path) -> None:
    """The CSV should contain the required header and aggregated row."""
    counts, _ = count_requests([VALID_LINE, VALID_LINE])
    output_path = tmp_path / "nested" / "status_by_hour.csv"

    write_csv(counts, output_path)

    assert output_path.read_text(encoding="utf-8").splitlines() == [
        "hour,status,count",
        "2026-11-09T08:00:00+05:30,200,2",
    ]
