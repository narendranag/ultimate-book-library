"""Tests for SQLite database generation."""

import sqlite3

from ultimate_book_library.database import build_database, load_library
from ultimate_book_library.schema import BookEntry, BookLibrary


class TestLoadLibrary:
    def test_load_valid_json(self, tmp_path):
        data_file = tmp_path / "books.json"
        data_file.write_text(
            '{"version": "1.0", "books": [{"title": "Test", "authors": ["Author"]}]}'
        )
        lib = load_library(data_file)
        assert len(lib.books) == 1
        assert lib.books[0].title == "Test"

    def test_load_missing_file(self, tmp_path):
        import pytest

        with pytest.raises(FileNotFoundError):
            load_library(tmp_path / "nonexistent.json")

    def test_load_seed_data(self):
        """Verify the actual seed data file loads and validates."""
        from ultimate_book_library.database import DEFAULT_DATA_PATH

        lib = load_library(DEFAULT_DATA_PATH)
        assert len(lib.books) >= 50


class TestBuildDatabase:
    def test_creates_database(self, tmp_path):
        library = BookLibrary(
            books=[
                BookEntry(
                    title="Test Book",
                    authors=["Author One"],
                    year_published=2020,
                    isbn_13="9781234567890",
                    genres=["Fiction"],
                ),
            ]
        )

        db_path = tmp_path / "test.db"
        result = build_database(library, db_path)

        assert result == db_path
        assert db_path.exists()

        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT COUNT(*) FROM books")
        assert cursor.fetchone()[0] == 1

        cursor = conn.execute("SELECT title, authors, isbn_13, genres FROM books")
        row = cursor.fetchone()
        assert row[0] == "Test Book"
        assert row[1] == "Author One"
        assert row[2] == "9781234567890"
        assert row[3] == "Fiction"
        conn.close()

    def test_multiple_authors_joined(self, tmp_path):
        library = BookLibrary(
            books=[
                BookEntry(title="Collab", authors=["Author A", "Author B"]),
            ]
        )

        db_path = tmp_path / "test.db"
        build_database(library, db_path)

        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT authors FROM books")
        assert cursor.fetchone()[0] == "Author A|Author B"
        conn.close()

    def test_overwrites_existing_database(self, tmp_path):
        library = BookLibrary(books=[BookEntry(title="Book 1", authors=["Author"])])

        db_path = tmp_path / "test.db"
        build_database(library, db_path)
        build_database(library, db_path)

        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT COUNT(*) FROM books")
        assert cursor.fetchone()[0] == 1  # Not duplicated
        conn.close()

    def test_empty_library(self, tmp_path):
        library = BookLibrary(books=[])
        db_path = tmp_path / "test.db"
        build_database(library, db_path)

        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT COUNT(*) FROM books")
        assert cursor.fetchone()[0] == 0
        conn.close()
