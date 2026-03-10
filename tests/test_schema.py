"""Tests for the Pydantic book schema."""

import pytest
from pydantic import ValidationError

from ultimate_book_library.schema import BookEntry, BookLibrary


class TestBookEntry:
    def test_minimal_book(self):
        book = BookEntry(title="Test Book", authors=["Author"])
        assert book.title == "Test Book"
        assert book.authors == ["Author"]
        assert book.genres == []
        assert book.language == "en"
        assert book.source == "manual"

    def test_full_book(self):
        book = BookEntry(
            title="Test Book",
            authors=["Author One", "Author Two"],
            year_published=2020,
            isbn_13="9781234567890",
            isbn_10="1234567890",
            genres=["Fiction", "Fantasy"],
            language="en",
            description="A test book.",
            page_count=300,
        )
        assert book.isbn_13 == "9781234567890"
        assert len(book.authors) == 2
        assert len(book.genres) == 2
        assert book.page_count == 300

    def test_missing_title_raises(self):
        with pytest.raises(ValidationError):
            BookEntry(authors=["Author"])  # type: ignore[call-arg]

    def test_missing_authors_raises(self):
        with pytest.raises(ValidationError):
            BookEntry(title="Test")  # type: ignore[call-arg]


class TestBookLibrary:
    def test_empty_library(self):
        lib = BookLibrary(books=[])
        assert lib.version == "1.0"
        assert len(lib.books) == 0

    def test_library_with_books(self):
        lib = BookLibrary(
            books=[
                BookEntry(title="Book 1", authors=["Author 1"]),
                BookEntry(title="Book 2", authors=["Author 2"]),
            ]
        )
        assert len(lib.books) == 2

    def test_library_from_dict(self):
        data = {
            "version": "1.0",
            "books": [
                {"title": "Test", "authors": ["Author"], "genres": ["Fiction"]},
            ],
        }
        lib = BookLibrary.model_validate(data)
        assert len(lib.books) == 1
        assert lib.books[0].genres == ["Fiction"]
