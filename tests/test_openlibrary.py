"""Tests for the Open Library API client."""

from unittest.mock import patch

import requests
import responses

from ultimate_book_library.models import Book
from ultimate_book_library.openlibrary import OPEN_LIBRARY_SEARCH_URL, OpenLibraryClient


class TestSearchISBN:
    @responses.activate
    def test_found_both_isbns(self, openlibrary_response_both_isbns):
        responses.add(
            responses.GET,
            OPEN_LIBRARY_SEARCH_URL,
            json=openlibrary_response_both_isbns,
            status=200,
        )

        client = OpenLibraryClient(rate_limit_seconds=0)
        result = client.search_isbn(Book(title="The Lord of the Rings", author="J.R.R. Tolkien"))

        assert result.isbn_13 == "9780618640157"
        assert result.isbn_10 == "0618640150"
        assert result.source == "OpenLibrary API"

    @responses.activate
    def test_found_isbn13_only(self, openlibrary_response_isbn13_only):
        responses.add(
            responses.GET,
            OPEN_LIBRARY_SEARCH_URL,
            json=openlibrary_response_isbn13_only,
            status=200,
        )

        client = OpenLibraryClient(rate_limit_seconds=0)
        result = client.search_isbn(Book(title="Some Book", author="Some Author"))

        assert result.isbn_13 == "9781234567890"
        assert result.isbn_10 == ""
        assert result.source == "OpenLibrary API"

    @responses.activate
    def test_not_found(self, openlibrary_response_not_found):
        responses.add(
            responses.GET,
            OPEN_LIBRARY_SEARCH_URL,
            json=openlibrary_response_not_found,
            status=200,
        )

        client = OpenLibraryClient(rate_limit_seconds=0)
        result = client.search_isbn(Book(title="Nonexistent Book", author="Nobody"))

        assert result.isbn_13 == ""
        assert result.isbn_10 == ""
        assert result.source == "Not found"

    @responses.activate
    def test_no_isbn_in_results(self, openlibrary_response_no_isbn):
        responses.add(
            responses.GET,
            OPEN_LIBRARY_SEARCH_URL,
            json=openlibrary_response_no_isbn,
            status=200,
        )

        client = OpenLibraryClient(rate_limit_seconds=0)
        result = client.search_isbn(Book(title="Old Book", author="Old Author"))

        assert result.source == "Not found"

    @responses.activate
    def test_api_error(self):
        responses.add(
            responses.GET,
            OPEN_LIBRARY_SEARCH_URL,
            status=500,
        )

        client = OpenLibraryClient(rate_limit_seconds=0)
        result = client.search_isbn(Book(title="Test", author="Test"))

        assert result.source == "API Error: 500"

    @responses.activate
    def test_network_error(self):
        responses.add(
            responses.GET,
            OPEN_LIBRARY_SEARCH_URL,
            body=requests.ConnectionError("Network unreachable"),
        )

        client = OpenLibraryClient(rate_limit_seconds=0)
        result = client.search_isbn(Book(title="Test", author="Test"))

        assert "Error:" in result.source

    @responses.activate
    def test_uses_year_when_provided(self, openlibrary_response_both_isbns):
        responses.add(
            responses.GET,
            OPEN_LIBRARY_SEARCH_URL,
            json=openlibrary_response_both_isbns,
            status=200,
        )

        client = OpenLibraryClient(rate_limit_seconds=0)
        client.search_isbn(Book(title="Test", author="Test", year="2020"))

        assert "publish_year=2020" in responses.calls[0].request.url

    @responses.activate
    def test_skips_year_when_empty(self, openlibrary_response_both_isbns):
        responses.add(
            responses.GET,
            OPEN_LIBRARY_SEARCH_URL,
            json=openlibrary_response_both_isbns,
            status=200,
        )

        client = OpenLibraryClient(rate_limit_seconds=0)
        client.search_isbn(Book(title="Test", author="Test", year=""))

        assert "publish_year" not in responses.calls[0].request.url

    @patch("ultimate_book_library.openlibrary.time.sleep")
    @responses.activate
    def test_rate_limiting(self, mock_sleep, openlibrary_response_both_isbns):
        responses.add(
            responses.GET,
            OPEN_LIBRARY_SEARCH_URL,
            json=openlibrary_response_both_isbns,
            status=200,
        )
        responses.add(
            responses.GET,
            OPEN_LIBRARY_SEARCH_URL,
            json=openlibrary_response_both_isbns,
            status=200,
        )

        client = OpenLibraryClient(rate_limit_seconds=2.0)
        client.search_isbn(Book(title="Book 1", author="Author 1"))
        client.search_isbn(Book(title="Book 2", author="Author 2"))

        # sleep should have been called for rate limiting on the second request
        assert mock_sleep.called
