"""FastAPI application for the Ultimate Book Library."""

from collections import Counter
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from ultimate_book_library.database import load_library
from ultimate_book_library.schema import BookEntry, BookLibrary

_library: BookLibrary | None = None


def get_library() -> BookLibrary:
    """Get the loaded library, loading from disk on first access."""
    global _library
    if _library is None:
        _library = load_library()
    return _library


def create_app(data_path: Path | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        global _library
        _library = load_library(data_path)
        yield

    app = FastAPI(
        title="Ultimate Book Library API",
        description="A curated collection of the best books in the world.",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(_build_router())

    # Mount web frontend and static files
    try:
        from fastapi.staticfiles import StaticFiles

        from ultimate_book_library.api.web import router as web_router

        static_dir = Path(__file__).parent / "static"
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
        app.include_router(web_router)
    except ImportError:
        pass  # Jinja2 not installed, skip web frontend

    return app


def _build_router():
    """Build the API router with all endpoints."""
    from fastapi import APIRouter

    router = APIRouter(prefix="/api")

    # -- Response models --

    class BookResponse(BaseModel):
        title: str
        authors: list[str]
        year_published: int | None = None
        isbn_13: str | None = None
        isbn_10: str | None = None
        genres: list[str]
        language: str
        description: str | None = None
        cover_url: str | None = None
        page_count: int | None = None

    class PaginatedBooks(BaseModel):
        total: int
        page: int
        page_size: int
        books: list[BookResponse]

    class StatsResponse(BaseModel):
        total_books: int
        total_pages: int
        year_range: list[int | None]
        isbn_coverage: float
        genres: dict[str, int]
        languages: dict[str, int]

    def _book_to_response(book: BookEntry) -> BookResponse:
        return BookResponse(
            title=book.title,
            authors=book.authors,
            year_published=book.year_published,
            isbn_13=book.isbn_13,
            isbn_10=book.isbn_10,
            genres=book.genres,
            language=book.language,
            description=book.description,
            cover_url=book.cover_url,
            page_count=book.page_count,
        )

    # -- Endpoints --

    @router.get("/books", response_model=PaginatedBooks)
    async def list_books(
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(20, ge=1, le=100, description="Items per page"),
        genre: str | None = Query(None, description="Filter by genre"),
        language: str | None = Query(None, description="Filter by language code"),
        year_min: int | None = Query(None, description="Minimum publication year"),
        year_max: int | None = Query(None, description="Maximum publication year"),
    ) -> PaginatedBooks:
        """List books with pagination and optional filters."""
        library = get_library()
        books = library.books

        if genre:
            genre_lower = genre.lower()
            books = [b for b in books if any(genre_lower in g.lower() for g in b.genres)]
        if language:
            books = [b for b in books if b.language == language]
        if year_min is not None:
            books = [b for b in books if b.year_published and b.year_published >= year_min]
        if year_max is not None:
            books = [b for b in books if b.year_published and b.year_published <= year_max]

        total = len(books)
        start = (page - 1) * page_size
        end = start + page_size
        page_books = books[start:end]

        return PaginatedBooks(
            total=total,
            page=page,
            page_size=page_size,
            books=[_book_to_response(b) for b in page_books],
        )

    @router.get("/books/{isbn}", response_model=BookResponse)
    async def get_book(isbn: str) -> BookResponse:
        """Get a single book by ISBN-13 or ISBN-10."""
        library = get_library()
        for book in library.books:
            if book.isbn_13 == isbn or book.isbn_10 == isbn:
                return _book_to_response(book)
        raise HTTPException(status_code=404, detail=f"Book not found: {isbn}")

    @router.get("/search", response_model=list[BookResponse])
    async def search_books(
        q: str = Query(..., min_length=1, description="Search query"),
        field: str | None = Query(None, description="Limit to field: title, author, genre"),
        limit: int = Query(20, ge=1, le=100, description="Max results"),
    ) -> list[BookResponse]:
        """Full-text search across books."""
        library = get_library()
        q_lower = q.lower()
        results: list[BookEntry] = []

        for book in library.books:
            if field == "title":
                match = q_lower in book.title.lower()
            elif field == "author":
                match = any(q_lower in a.lower() for a in book.authors)
            elif field == "genre":
                match = any(q_lower in g.lower() for g in book.genres)
            else:
                match = (
                    q_lower in book.title.lower()
                    or any(q_lower in a.lower() for a in book.authors)
                    or any(q_lower in g.lower() for g in book.genres)
                )

            if match:
                results.append(book)
                if len(results) >= limit:
                    break

        return [_book_to_response(b) for b in results]

    @router.get("/stats", response_model=StatsResponse)
    async def get_stats() -> StatsResponse:
        """Get collection statistics."""
        library = get_library()
        books = library.books

        years = [b.year_published for b in books if b.year_published is not None]
        pages = [b.page_count for b in books if b.page_count]
        with_isbn = sum(1 for b in books if b.isbn_13 or b.isbn_10)

        genre_counter: Counter[str] = Counter()
        lang_counter: Counter[str] = Counter()
        for book in books:
            for g in book.genres:
                genre_counter[g] += 1
            lang_counter[book.language] += 1

        return StatsResponse(
            total_books=len(books),
            total_pages=sum(pages) if pages else 0,
            year_range=[min(years), max(years)] if years else [None, None],
            isbn_coverage=with_isbn / len(books) if books else 0.0,
            genres=dict(genre_counter.most_common()),
            languages=dict(lang_counter.most_common()),
        )

    return router


# Default app instance for `uvicorn ultimate_book_library.api.app:app`
app = create_app()
