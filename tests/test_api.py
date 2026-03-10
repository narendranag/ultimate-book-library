"""Tests for the FastAPI REST API."""

import pytest
from httpx import ASGITransport, AsyncClient

from ultimate_book_library.api.app import create_app


@pytest.fixture
def api_app():
    """Create a test API app using the seed data."""
    return create_app()


@pytest.fixture
async def client(api_app):
    """Create an async HTTP client for testing."""
    async with AsyncClient(transport=ASGITransport(app=api_app), base_url="http://test") as ac:
        yield ac


class TestListBooks:
    @pytest.mark.anyio
    async def test_list_default(self, client):
        resp = await client.get("/api/books")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 50
        assert data["page"] == 1
        assert len(data["books"]) == 20

    @pytest.mark.anyio
    async def test_list_pagination(self, client):
        resp = await client.get("/api/books?page=2&page_size=10")
        assert resp.status_code == 200
        data = resp.json()
        assert data["page"] == 2
        assert len(data["books"]) == 10

    @pytest.mark.anyio
    async def test_filter_by_genre(self, client):
        resp = await client.get("/api/books?genre=Fantasy")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] > 0
        for book in data["books"]:
            assert any("fantasy" in g.lower() for g in book["genres"])

    @pytest.mark.anyio
    async def test_filter_by_language(self, client):
        resp = await client.get("/api/books?language=ru")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] > 0
        for book in data["books"]:
            assert book["language"] == "ru"


class TestGetBook:
    @pytest.mark.anyio
    async def test_get_by_isbn_13(self, client):
        resp = await client.get("/api/books/9780061120084")
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "To Kill a Mockingbird"

    @pytest.mark.anyio
    async def test_get_by_isbn_10(self, client):
        resp = await client.get("/api/books/0061120081")
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "To Kill a Mockingbird"

    @pytest.mark.anyio
    async def test_not_found(self, client):
        resp = await client.get("/api/books/0000000000")
        assert resp.status_code == 404


class TestSearch:
    @pytest.mark.anyio
    async def test_search_by_query(self, client):
        resp = await client.get("/api/search?q=tolkien")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 2

    @pytest.mark.anyio
    async def test_search_by_field(self, client):
        resp = await client.get("/api/search?q=dystopian&field=genre")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0

    @pytest.mark.anyio
    async def test_search_limit(self, client):
        resp = await client.get("/api/search?q=fiction&limit=3")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) <= 3

    @pytest.mark.anyio
    async def test_search_no_results(self, client):
        resp = await client.get("/api/search?q=zzzznonexistent")
        assert resp.status_code == 200
        assert resp.json() == []


class TestStats:
    @pytest.mark.anyio
    async def test_stats(self, client):
        resp = await client.get("/api/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_books"] >= 50
        assert data["total_pages"] > 0
        assert "Fiction" in data["genres"]
        assert "en" in data["languages"]
        assert data["isbn_coverage"] == 1.0
