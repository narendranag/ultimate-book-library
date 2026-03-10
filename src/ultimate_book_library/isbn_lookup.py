"""CSV processing for batch ISBN lookups."""

import csv
import logging
from pathlib import Path

from ultimate_book_library.models import Book
from ultimate_book_library.openlibrary import OpenLibraryClient

logger = logging.getLogger(__name__)


def detect_columns(fieldnames: list[str]) -> dict[str, str | None]:
    """Detect title, author, and year columns from CSV headers.

    Returns a dict with keys 'title', 'author', 'year' mapped to column names.
    """
    result: dict[str, str | None] = {"title": None, "author": None, "year": None}

    for field in fieldnames:
        lower_field = field.lower()
        if "title" in lower_field and result["title"] is None:
            result["title"] = field
        elif "author" in lower_field and result["author"] is None:
            result["author"] = field
        elif (
            any(term in lower_field for term in ["year", "date", "published"])
            and result["year"] is None
        ):
            result["year"] = field

    return result


def process_csv(
    input_file: str,
    output_file: str,
    client: OpenLibraryClient | None = None,
) -> None:
    """Process an input CSV and create an output CSV with ISBNs."""
    if client is None:
        client = OpenLibraryClient()

    input_path = Path(input_file)
    if not input_path.exists():
        logger.error("Input file '%s' not found", input_file)
        return

    with open(input_path, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        if not fieldnames:
            logger.error("Input CSV appears to be empty")
            return

        columns = detect_columns(list(fieldnames))

        if not columns["title"]:
            logger.error("Could not identify title column")
            return

        if not columns["author"]:
            logger.error("Could not identify author column")
            return

        # Read all rows into memory to get count and avoid double-open
        rows = list(reader)
        total_books = len(rows)

    # Build output fieldnames
    output_fieldnames = list(fieldnames)
    if not any("isbn-13" in f.lower() for f in output_fieldnames):
        output_fieldnames.append("ISBN-13")
    if not any("isbn-10" in f.lower() for f in output_fieldnames):
        output_fieldnames.append("ISBN-10")
    output_fieldnames.append("ISBN_Source")

    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=output_fieldnames)
        writer.writeheader()

        for i, row in enumerate(rows, 1):
            title = row.get(columns["title"], "")  # type: ignore[arg-type]
            author = row.get(columns["author"], "")  # type: ignore[arg-type]
            year = row.get(columns["year"], "") if columns["year"] else ""  # type: ignore[arg-type]

            if not title or not author:
                logger.info("Skipping row %d: Missing title or author", i)
                row["ISBN-13"] = ""
                row["ISBN-10"] = ""
                row["ISBN_Source"] = "Missing data"
                writer.writerow(row)
                continue

            logger.info("Processing %d/%d: %s by %s", i, total_books, title, author)

            book = Book(title=title, author=author, year=year)
            result = client.search_isbn(book)

            row["ISBN-13"] = result.isbn_13
            row["ISBN-10"] = result.isbn_10
            row["ISBN_Source"] = result.source
            writer.writerow(row)

    logger.info("Processing complete! Output written to: %s", output_file)
