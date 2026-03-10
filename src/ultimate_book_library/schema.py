"""Pydantic models for the book library schema."""

from datetime import date

from pydantic import BaseModel, Field


class BookEntry(BaseModel):
    """A book in the curated library."""

    # Core metadata
    title: str
    authors: list[str]
    year_published: int | None = None

    # Identifiers
    isbn_13: str | None = None
    isbn_10: str | None = None

    # Classification
    genres: list[str] = Field(default_factory=list)
    language: str = "en"

    # Enrichment
    description: str | None = None
    cover_url: str | None = None
    page_count: int | None = None

    # Source tracking
    source: str = "manual"
    date_added: date | None = None


class BookLibrary(BaseModel):
    """The complete book library."""

    version: str = "1.0"
    books: list[BookEntry]
