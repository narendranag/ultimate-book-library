"""Validation utilities for the book library data."""

import logging
from collections import Counter

from ultimate_book_library.schema import BookLibrary

logger = logging.getLogger(__name__)


def validate_library(library: BookLibrary) -> list[str]:
    """Validate a book library and return a list of warnings/issues.

    Returns an empty list if no issues are found.
    """
    issues: list[str] = []

    if not library.books:
        issues.append("Library is empty")
        return issues

    # Check for duplicate ISBNs
    isbn_13s = [b.isbn_13 for b in library.books if b.isbn_13]
    isbn_13_dupes = [isbn for isbn, count in Counter(isbn_13s).items() if count > 1]
    for isbn in isbn_13_dupes:
        issues.append(f"Duplicate ISBN-13: {isbn}")

    isbn_10s = [b.isbn_10 for b in library.books if b.isbn_10]
    isbn_10_dupes = [isbn for isbn, count in Counter(isbn_10s).items() if count > 1]
    for isbn in isbn_10_dupes:
        issues.append(f"Duplicate ISBN-10: {isbn}")

    # Check for books missing ISBNs
    missing_isbn = [b for b in library.books if not b.isbn_13 and not b.isbn_10]
    if missing_isbn:
        issues.append(f"{len(missing_isbn)} book(s) missing both ISBN-13 and ISBN-10")

    # Check for books missing key metadata
    for book in library.books:
        if not book.authors:
            issues.append(f"Book '{book.title}' has no authors")
        if not book.genres:
            issues.append(f"Book '{book.title}' has no genres")

    return issues
