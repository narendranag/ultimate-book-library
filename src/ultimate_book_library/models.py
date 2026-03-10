"""Data models for book metadata and ISBN lookup results."""

from dataclasses import dataclass


@dataclass
class Book:
    """A book with core metadata for ISBN lookup."""

    title: str
    author: str
    year: str | None = None


@dataclass
class ISBNResult:
    """Result of an ISBN lookup."""

    isbn_13: str = ""
    isbn_10: str = ""
    source: str = ""
