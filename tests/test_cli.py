"""Tests for the Typer CLI."""

import json

from typer.testing import CliRunner

from ultimate_book_library.cli import app

runner = CliRunner()


class TestHelp:
    def test_help(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "find-isbn" in result.output
        assert "build-db" in result.output
        assert "validate" in result.output
        assert "list" in result.output
        assert "search" in result.output
        assert "add" in result.output
        assert "stats" in result.output
        assert "export" in result.output

    def test_find_isbn_help(self):
        result = runner.invoke(app, ["find-isbn", "--help"])
        assert result.exit_code == 0
        assert "INPUT_FILE" in result.output
        assert "--rate-limit" in result.output


class TestValidate:
    def test_validate_seed_data(self):
        result = runner.invoke(app, ["validate", "--data", "data/books.json"])
        assert result.exit_code == 0
        assert "No issues found" in result.output

    def test_validate_missing_file(self):
        result = runner.invoke(app, ["validate", "--data", "nonexistent.json"])
        assert result.exit_code == 1


class TestBuildDB:
    def test_build_db(self, tmp_path):
        db_path = tmp_path / "test.db"
        result = runner.invoke(
            app, ["build-db", "--data", "data/books.json", "--output", str(db_path)]
        )
        assert result.exit_code == 0
        assert "Database built" in result.output
        assert db_path.exists()


class TestListBooks:
    def test_list_default(self):
        result = runner.invoke(app, ["list", "--data", "data/books.json"])
        assert result.exit_code == 0
        assert "Books" in result.output

    def test_list_filter_genre(self):
        result = runner.invoke(app, ["list", "--data", "data/books.json", "--genre", "Fantasy"])
        assert result.exit_code == 0
        assert "Tolkien" in result.output

    def test_list_filter_language(self):
        result = runner.invoke(app, ["list", "--data", "data/books.json", "--language", "ru"])
        assert result.exit_code == 0
        assert "Dostoevsky" in result.output

    def test_list_no_match(self):
        result = runner.invoke(
            app, ["list", "--data", "data/books.json", "--genre", "nonexistent_genre_xyz"]
        )
        assert result.exit_code == 0
        assert "No books match" in result.output


class TestSearch:
    def test_search_by_title(self):
        result = runner.invoke(app, ["search", "Hobbit", "--data", "data/books.json"])
        assert result.exit_code == 0
        assert "Hobbit" in result.output

    def test_search_by_author(self):
        result = runner.invoke(
            app, ["search", "Tolkien", "--data", "data/books.json", "--field", "author"]
        )
        assert result.exit_code == 0
        assert "Tolkien" in result.output

    def test_search_by_genre(self):
        result = runner.invoke(
            app, ["search", "Dystopian", "--data", "data/books.json", "--field", "genre"]
        )
        assert result.exit_code == 0
        assert "1984" in result.output

    def test_search_no_results(self):
        result = runner.invoke(app, ["search", "zzzznonexistent", "--data", "data/books.json"])
        assert result.exit_code == 0
        assert "No books found" in result.output


class TestAdd:
    def test_add_book(self, tmp_path):
        data_path = tmp_path / "books.json"
        data_path.write_text('{"version": "1.0", "books": []}')

        result = runner.invoke(
            app,
            [
                "add",
                "New Book",
                "--author",
                "Test Author",
                "--year",
                "2024",
                "--genre",
                "Fiction",
                "--data",
                str(data_path),
            ],
        )
        assert result.exit_code == 0
        assert "Added" in result.output

        # Verify it was written
        data = json.loads(data_path.read_text())
        assert len(data["books"]) == 1
        assert data["books"][0]["title"] == "New Book"

    def test_add_book_creates_file(self, tmp_path):
        data_path = tmp_path / "new_books.json"

        result = runner.invoke(
            app,
            [
                "add",
                "First Book",
                "--author",
                "Author",
                "--data",
                str(data_path),
            ],
        )
        assert result.exit_code == 0
        assert data_path.exists()


class TestStats:
    def test_stats(self):
        result = runner.invoke(app, ["stats", "--data", "data/books.json"])
        assert result.exit_code == 0
        assert "Total books" in result.output
        assert "Top Genres" in result.output
        assert "Languages" in result.output
        assert "ISBN coverage" in result.output


class TestExport:
    def test_export_csv(self, tmp_path):
        out = tmp_path / "books.csv"
        result = runner.invoke(
            app, ["export", str(out), "--format", "csv", "--data", "data/books.json"]
        )
        assert result.exit_code == 0
        content = out.read_text()
        assert "Title" in content
        assert "Tolkien" in content

    def test_export_json(self, tmp_path):
        out = tmp_path / "books.json"
        result = runner.invoke(
            app, ["export", str(out), "--format", "json", "--data", "data/books.json"]
        )
        assert result.exit_code == 0
        data = json.loads(out.read_text())
        assert isinstance(data, list)
        assert len(data) == 50

    def test_export_markdown(self, tmp_path):
        out = tmp_path / "books.md"
        result = runner.invoke(
            app, ["export", str(out), "--format", "markdown", "--data", "data/books.json"]
        )
        assert result.exit_code == 0
        content = out.read_text()
        assert "| Title" in content
        assert "Tolkien" in content

    def test_export_unknown_format(self, tmp_path):
        out = tmp_path / "books.xyz"
        result = runner.invoke(
            app, ["export", str(out), "--format", "xyz", "--data", "data/books.json"]
        )
        assert result.exit_code == 1
