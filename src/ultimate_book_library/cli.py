"""Command-line interface for the Ultimate Book Library."""

import argparse
import logging

from ultimate_book_library.isbn_lookup import process_csv
from ultimate_book_library.openlibrary import OpenLibraryClient


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Ultimate Book Library - tools to find, enrich, and manage book data.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # find-isbn command
    isbn_parser = subparsers.add_parser(
        "find-isbn",
        help="Find ISBNs for books in a CSV file",
    )
    isbn_parser.add_argument("input_file", help="Input CSV file with books")
    isbn_parser.add_argument("output_file", help="Output CSV file to write results")
    isbn_parser.add_argument(
        "--rate-limit",
        type=float,
        default=1.0,
        help="Seconds between API requests (default: 1.0)",
    )
    isbn_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Configure logging
    log_level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(level=log_level, format="%(message)s")

    if args.command == "find-isbn":
        client = OpenLibraryClient(rate_limit_seconds=args.rate_limit)
        process_csv(args.input_file, args.output_file, client=client)
