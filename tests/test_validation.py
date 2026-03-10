"""Tests for book library validation."""

from ultimate_book_library.schema import BookEntry, BookLibrary
from ultimate_book_library.validation import validate_library


class TestValidateLibrary:
    def test_valid_library(self):
        library = BookLibrary(
            books=[
                BookEntry(
                    title="Book",
                    authors=["Author"],
                    isbn_13="9781234567890",
                    genres=["Fiction"],
                ),
            ]
        )
        issues = validate_library(library)
        assert issues == []

    def test_empty_library(self):
        library = BookLibrary(books=[])
        issues = validate_library(library)
        assert "Library is empty" in issues

    def test_duplicate_isbn_13(self):
        library = BookLibrary(
            books=[
                BookEntry(
                    title="Book 1",
                    authors=["Author"],
                    isbn_13="9781234567890",
                    genres=["Fiction"],
                ),
                BookEntry(
                    title="Book 2",
                    authors=["Author"],
                    isbn_13="9781234567890",
                    genres=["Fiction"],
                ),
            ]
        )
        issues = validate_library(library)
        assert any("Duplicate ISBN-13" in i for i in issues)

    def test_duplicate_isbn_10(self):
        library = BookLibrary(
            books=[
                BookEntry(
                    title="Book 1",
                    authors=["Author"],
                    isbn_10="1234567890",
                    genres=["Fiction"],
                ),
                BookEntry(
                    title="Book 2",
                    authors=["Author"],
                    isbn_10="1234567890",
                    genres=["Fiction"],
                ),
            ]
        )
        issues = validate_library(library)
        assert any("Duplicate ISBN-10" in i for i in issues)

    def test_missing_isbn(self):
        library = BookLibrary(
            books=[
                BookEntry(title="No ISBN Book", authors=["Author"], genres=["Fiction"]),
            ]
        )
        issues = validate_library(library)
        assert any("missing both ISBN" in i for i in issues)

    def test_missing_genres(self):
        library = BookLibrary(
            books=[
                BookEntry(title="No Genre", authors=["Author"], isbn_13="9781234567890"),
            ]
        )
        issues = validate_library(library)
        assert any("no genres" in i for i in issues)

    def test_missing_authors(self):
        library = BookLibrary(
            books=[
                BookEntry(title="Orphan Book", authors=[], isbn_13="9781234567890", genres=["X"]),
            ]
        )
        issues = validate_library(library)
        assert any("no authors" in i for i in issues)

    def test_seed_data_validates(self):
        """Verify the actual seed data passes validation."""
        from ultimate_book_library.database import DEFAULT_DATA_PATH, load_library

        library = load_library(DEFAULT_DATA_PATH)
        issues = validate_library(library)
        assert issues == [], f"Seed data has issues: {issues}"
