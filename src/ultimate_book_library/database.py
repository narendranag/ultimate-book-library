"""SQLite database generation from book library JSON."""

import json
import logging
import sqlite3
from pathlib import Path

from ultimate_book_library.schema import BookEntry, BookLibrary

logger = logging.getLogger(__name__)

DEFAULT_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "books.json"
DEFAULT_DB_PATH = Path(__file__).parent.parent.parent / "books.db"


def load_library(data_path: Path | None = None) -> BookLibrary:
    """Load and validate the book library from a JSON file."""
    path = data_path or DEFAULT_DATA_PATH

    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    return BookLibrary.model_validate(data)


def build_database(library: BookLibrary, db_path: Path | None = None) -> Path:
    """Build a SQLite database from a BookLibrary."""
    path = db_path or DEFAULT_DB_PATH

    # Remove existing database
    if path.exists():
        path.unlink()

    conn = sqlite3.connect(path)
    try:
        _create_tables(conn)
        _insert_books(conn, library.books)
        conn.commit()
        logger.info("Database built with %d books at %s", len(library.books), path)
    finally:
        conn.close()

    return path


def _create_tables(conn: sqlite3.Connection) -> None:
    """Create the database schema."""
    conn.executescript("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            authors TEXT NOT NULL,
            year_published INTEGER,
            isbn_13 TEXT,
            isbn_10 TEXT,
            genres TEXT,
            language TEXT DEFAULT 'en',
            description TEXT,
            cover_url TEXT,
            page_count INTEGER,
            source TEXT DEFAULT 'manual',
            date_added TEXT
        );

        CREATE INDEX idx_books_title ON books(title);
        CREATE INDEX idx_books_isbn_13 ON books(isbn_13);
        CREATE INDEX idx_books_isbn_10 ON books(isbn_10);
        CREATE INDEX idx_books_language ON books(language);
    """)


def _insert_books(conn: sqlite3.Connection, books: list[BookEntry]) -> None:
    """Insert books into the database."""
    for book in books:
        conn.execute(
            """
            INSERT INTO books (
                title, authors, year_published, isbn_13, isbn_10,
                genres, language, description, cover_url, page_count,
                source, date_added
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                book.title,
                "|".join(book.authors),
                book.year_published,
                book.isbn_13,
                book.isbn_10,
                "|".join(book.genres),
                book.language,
                book.description,
                book.cover_url,
                book.page_count,
                book.source,
                book.date_added.isoformat() if book.date_added else None,
            ),
        )
