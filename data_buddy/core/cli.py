"""Command-line entry point for Data Buddy."""

from __future__ import annotations

import argparse

from data_buddy import Buddy


def main() -> None:
    """Run a simplified Data Buddy CLI workflow."""
    parser = argparse.ArgumentParser(description="Data Buddy no-code data workflow")
    parser.add_argument("file", help="Path or URL to dataset")
    parser.add_argument("--target", help="Optional target column for insight", default=None)
    args = parser.parse_args()

    buddy = Buddy().load(args.file).clean()
    print("Data loaded and cleaned successfully.")
    print("Detection summary:", buddy.detect())
    print("Insights:", buddy.insight(target=args.target))


if __name__ == "__main__":
    main()
