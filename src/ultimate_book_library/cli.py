"""Command-line interface for the Ultimate Book Library."""

import argparse
import logging
from pathlib import Path

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

    # build-db command
    db_parser = subparsers.add_parser(
        "build-db",
        help="Build SQLite database from book data",
    )
    db_parser.add_argument(
        "--data",
        type=str,
        default=None,
        help="Path to books.json (default: data/books.json)",
    )
    db_parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output database path (default: books.db)",
    )
    db_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    # validate command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate book library data",
    )
    validate_parser.add_argument(
        "--data",
        type=str,
        default=None,
        help="Path to books.json (default: data/books.json)",
    )
    validate_parser.add_argument(
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

    elif args.command == "build-db":
        _run_build_db(args)

    elif args.command == "validate":
        _run_validate(args)


def _run_build_db(args: argparse.Namespace) -> None:
    """Run the build-db command."""
    from ultimate_book_library.database import build_database, load_library

    data_path = Path(args.data) if args.data else None
    db_path = Path(args.output) if args.output else None

    try:
        library = load_library(data_path)
        result_path = build_database(library, db_path)
        print(f"Database built successfully: {result_path}")
        print(f"  {len(library.books)} books loaded")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error building database: {e}")


def _run_validate(args: argparse.Namespace) -> None:
    """Run the validate command."""
    from ultimate_book_library.database import load_library
    from ultimate_book_library.validation import validate_library

    data_path = Path(args.data) if args.data else None

    try:
        library = load_library(data_path)
        issues = validate_library(library)

        print(f"Validated {len(library.books)} books")
        if issues:
            print(f"\nFound {len(issues)} issue(s):")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("No issues found!")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error validating data: {e}")
