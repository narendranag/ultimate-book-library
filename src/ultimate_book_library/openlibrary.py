"""Open Library API client for ISBN lookups."""

import logging
import time

import requests

from ultimate_book_library.cleaning import clean_author, clean_title
from ultimate_book_library.models import Book, ISBNResult

logger = logging.getLogger(__name__)

OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"


class OpenLibraryClient:
    """Client for searching books via the Open Library API."""

    def __init__(
        self,
        rate_limit_seconds: float = 1.0,
        max_results: int = 5,
        session: requests.Session | None = None,
    ):
        self.rate_limit_seconds = rate_limit_seconds
        self.max_results = max_results
        self.session = session or requests.Session()
        self._last_request_time: float = 0

    def _wait_for_rate_limit(self) -> None:
        """Wait if needed to respect API rate limits."""
        if self._last_request_time > 0:
            elapsed = time.time() - self._last_request_time
            if elapsed < self.rate_limit_seconds:
                time.sleep(self.rate_limit_seconds - elapsed)
        self._last_request_time = time.time()

    def search_isbn(self, book: Book) -> ISBNResult:
        """Search for a book's ISBN using the Open Library API."""
        clean_t = clean_title(book.title)
        clean_a = clean_author(book.author)

        params: dict[str, str | int] = {
            "title": clean_t,
            "author": clean_a,
            "limit": self.max_results,
        }

        if book.year and book.year.strip().isdigit():
            params["publish_year"] = book.year.strip()

        try:
            self._wait_for_rate_limit()
            response = self.session.get(OPEN_LIBRARY_SEARCH_URL, params=params)

            if response.status_code != 200:
                return ISBNResult(source=f"API Error: {response.status_code}")

            data = response.json()

            if data["numFound"] == 0:
                return ISBNResult(source="Not found")

            for doc in data["docs"]:
                isbn_13 = ""
                isbn_10 = ""

                if "isbn" in doc:
                    for isbn in doc["isbn"]:
                        if len(isbn) == 13 and not isbn_13:
                            isbn_13 = isbn
                        elif len(isbn) == 10 and not isbn_10:
                            isbn_10 = isbn

                        if isbn_13 and isbn_10:
                            break

                if isbn_13 or isbn_10:
                    return ISBNResult(
                        isbn_13=isbn_13,
                        isbn_10=isbn_10,
                        source="OpenLibrary API",
                    )

            return ISBNResult(source="Not found")

        except requests.RequestException as e:
            logger.error("API request failed: %s", e)
            return ISBNResult(source=f"Error: {e}")
