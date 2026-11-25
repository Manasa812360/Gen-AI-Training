#!/usr/bin/env python3
"""Cluster historical tickets with TF-IDF and KMeans."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Any, Sequence

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "tickets" / "tickets_history.csv"
OUTPUT_PATH = ROOT / "outputs" / "m07" / "clusters.csv"
REQUIRED_FIELDS = {
    "number",
    "short_description",
    "description",
    "handle_time_min",
}
OUTPUT_FIELDS = (
    "cluster_id",
    "size",
    "top_terms",
    "sample_tickets",
    "mean_handle_time_min",
)


def positive_integer(value: str) -> int:
    """Return a positive integer for argparse."""
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{value!r} is not an integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def load_tickets(input_path: Path) -> list[dict[str, str]]:
    """Load and validate historical ticket rows."""
    with input_path.open("r", encoding="utf-8", newline="") as input_file:
        reader = csv.DictReader(input_file)
        missing_fields = REQUIRED_FIELDS - set(reader.fieldnames or ())
        if missing_fields:
            raise ValueError(
                f"{input_path} is missing required columns: "
                f"{', '.join(sorted(missing_fields))}"
            )

        tickets = list(reader)
    if not tickets:
        raise ValueError(f"{input_path} contains no ticket rows")

    for line_number, ticket in enumerate(tickets, start=2):
        if not ticket["number"].strip():
            raise ValueError(f"{input_path}:{line_number} has an empty ticket number")
        text = f"{ticket['short_description']} {ticket['description']}".strip()
        if not text:
            raise ValueError(f"{input_path}:{line_number} has no ticket text")
        try:
            handle_time = float(ticket["handle_time_min"])
        except ValueError as exc:
            raise ValueError(
                f"{input_path}:{line_number} has invalid handle_time_min "
                f"{ticket['handle_time_min']!r}"
            ) from exc
        if handle_time < 0:
            raise ValueError(
                f"{input_path}:{line_number} has a negative handle_time_min"
            )

    return tickets


def cluster_tickets(
    tickets: list[dict[str, str]], k: int
) -> tuple[list[dict[str, Any]], list[str]]:
    """Cluster ticket text and return report rows plus feature terms."""
    if k > len(tickets):
        raise ValueError(
            f"k={k} cannot exceed the number of tickets ({len(tickets)})"
        )

    texts = [
        f"{ticket['short_description']} {ticket['description']}".strip()
        for ticket in tickets
    ]
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
    )
    vectors = vectorizer.fit_transform(texts)
    terms = vectorizer.get_feature_names_out().tolist()

    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(vectors)

    clustered: dict[int, list[int]] = defaultdict(list)
    for row_index, label in enumerate(labels):
        clustered[int(label)].append(row_index)

    rows: list[dict[str, Any]] = []
    for cluster_id in range(k):
        member_indices = clustered.get(cluster_id, [])
        weights = model.cluster_centers_[cluster_id]
        top_term_indices = sorted(
            range(len(terms)),
            key=lambda index: (-weights[index], terms[index]),
        )[:8]
        top_terms = [terms[index] for index in top_term_indices if weights[index] > 0]
        samples = [
            tickets[index]["number"]
            for index in sorted(member_indices)[:3]
        ]
        mean_handle_time = (
            sum(float(tickets[index]["handle_time_min"]) for index in member_indices)
            / len(member_indices)
            if member_indices
            else 0.0
        )
        rows.append(
            {
                "cluster_id": cluster_id,
                "size": len(member_indices),
                "top_terms": "; ".join(top_terms),
                "sample_tickets": "; ".join(samples),
                "mean_handle_time_min": f"{mean_handle_time:.2f}",
            }
        )

    rows.sort(key=lambda row: (-row["size"], row["cluster_id"]))
    return rows, terms


def write_clusters(rows: list[dict[str, Any]], output_path: Path) -> None:
    """Write cluster summaries to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def print_clusters(rows: list[dict[str, Any]]) -> None:
    """Print human-readable cluster summaries."""
    for row in rows:
        print(f"Cluster {row['cluster_id']}")
        print(f"  Size: {row['size']}")
        print(f"  Top terms: {row['top_terms']}")
        print(f"  Sample tickets: {row['sample_tickets']}")
        print(f"  Mean handle_time_min: {row['mean_handle_time_min']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--k",
        type=positive_integer,
        default=8,
        help="number of KMeans clusters (default: 8)",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=INPUT_PATH,
        help=f"historical ticket CSV (default: {INPUT_PATH})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help=f"cluster CSV to write (default: {OUTPUT_PATH})",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        tickets = load_tickets(args.input)
        rows, _ = cluster_tickets(tickets, args.k)
        write_clusters(rows, args.output)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Unable to cluster tickets: {exc}") from exc

    print_clusters(rows)
    print(f"Wrote {len(rows)} clusters to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
