"""Web routes for the HTML frontend."""

from collections import Counter
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ultimate_book_library.api.app import get_library
from ultimate_book_library.schema import BookEntry

TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()

LANGUAGE_NAMES = {
    "en": "English",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "ru": "Russian",
    "pt": "Portuguese",
    "zh": "Chinese",
    "el": "Greek",
    "he": "Hebrew",
    "nl": "Dutch",
}


def _get_all_genres(books: list[BookEntry]) -> list[str]:
    """Get sorted list of unique genres."""
    counter: Counter[str] = Counter()
    for book in books:
        for g in book.genres:
            counter[g] += 1
    return [g for g, _ in counter.most_common()]


def _get_all_languages(books: list[BookEntry]) -> list[tuple[str, str]]:
    """Get sorted list of (code, name) language pairs."""
    codes = sorted({b.language for b in books})
    return [(code, LANGUAGE_NAMES.get(code, code)) for code in codes]


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Home page with book grid and search."""
    library = get_library()
    books = library.books
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "books": books,
            "total": len(books),
            "genres": _get_all_genres(books),
            "languages": _get_all_languages(books),
        },
    )


@router.get("/search-results", response_class=HTMLResponse)
async def search_results(
    request: Request,
    q: str = "",
    genre: str = "",
    language: str = "",
) -> HTMLResponse:
    """HTMX endpoint returning partial book list HTML."""
    library = get_library()
    books = library.books

    if q:
        q_lower = q.lower()
        books = [
            b
            for b in books
            if q_lower in b.title.lower()
            or any(q_lower in a.lower() for a in b.authors)
            or any(q_lower in g.lower() for g in b.genres)
        ]

    if genre:
        genre_lower = genre.lower()
        books = [b for b in books if any(genre_lower in g.lower() for g in b.genres)]

    if language:
        books = [b for b in books if b.language == language]

    return templates.TemplateResponse(
        request,
        "partials/book_list.html",
        {"books": books},
    )


@router.get("/book/{isbn}", response_class=HTMLResponse)
async def book_detail(request: Request, isbn: str) -> HTMLResponse:
    """Book detail page."""
    library = get_library()
    for book in library.books:
        if book.isbn_13 == isbn or book.isbn_10 == isbn:
            return templates.TemplateResponse(
                request,
                "book_detail.html",
                {"book": book},
            )

    return templates.TemplateResponse(
        request,
        "book_detail.html",
        {"book": BookEntry(title="Book Not Found", authors=["Unknown"])},
    )
