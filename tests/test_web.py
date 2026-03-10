"""Tests for the web frontend routes."""

import pytest
from httpx import ASGITransport, AsyncClient

from ultimate_book_library.api.app import create_app


@pytest.fixture
def web_app():
    return create_app()


@pytest.fixture
async def client(web_app):
    async with AsyncClient(transport=ASGITransport(app=web_app), base_url="http://test") as ac:
        yield ac


class TestIndexPage:
    @pytest.mark.anyio
    async def test_index_returns_html(self, client):
        resp = await client.get("/")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]
        assert "Ultimate Book Library" in resp.text

    @pytest.mark.anyio
    async def test_index_contains_books(self, client):
        resp = await client.get("/")
        assert "book-card" in resp.text

    @pytest.mark.anyio
    async def test_index_has_search(self, client):
        resp = await client.get("/")
        assert 'name="q"' in resp.text
        assert "hx-get" in resp.text


class TestSearchResults:
    @pytest.mark.anyio
    async def test_search_by_query(self, client):
        resp = await client.get("/search-results?q=tolkien")
        assert resp.status_code == 200
        assert "Tolkien" in resp.text

    @pytest.mark.anyio
    async def test_filter_by_genre(self, client):
        resp = await client.get("/search-results?genre=Fantasy")
        assert resp.status_code == 200
        assert "Hobbit" in resp.text

    @pytest.mark.anyio
    async def test_filter_by_language(self, client):
        resp = await client.get("/search-results?language=ru")
        assert resp.status_code == 200
        assert "Dostoevsky" in resp.text

    @pytest.mark.anyio
    async def test_no_results(self, client):
        resp = await client.get("/search-results?q=zzzznonexistent")
        assert resp.status_code == 200
        assert "No books found" in resp.text


class TestBookDetail:
    @pytest.mark.anyio
    async def test_book_by_isbn(self, client):
        resp = await client.get("/book/9780061120084")
        assert resp.status_code == 200
        assert "To Kill a Mockingbird" in resp.text
        assert "Harper Lee" in resp.text

    @pytest.mark.anyio
    async def test_book_not_found(self, client):
        resp = await client.get("/book/0000000000")
        assert resp.status_code == 200
        assert "Book Not Found" in resp.text


class TestStaticFiles:
    @pytest.mark.anyio
    async def test_css_served(self, client):
        resp = await client.get("/static/styles.css")
        assert resp.status_code == 200
        assert "book-grid" in resp.text
