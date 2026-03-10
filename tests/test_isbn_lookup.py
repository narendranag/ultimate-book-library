"""Tests for CSV processing and ISBN lookup orchestration."""

from unittest.mock import MagicMock

from ultimate_book_library.isbn_lookup import detect_columns, process_csv
from ultimate_book_library.models import ISBNResult


class TestDetectColumns:
    def test_standard_columns(self):
        result = detect_columns(["Title", "Author", "Year"])
        assert result == {"title": "Title", "author": "Author", "year": "Year"}

    def test_case_insensitive(self):
        result = detect_columns(["TITLE", "AUTHOR", "YEAR"])
        assert result == {"title": "TITLE", "author": "AUTHOR", "year": "YEAR"}

    def test_partial_match(self):
        result = detect_columns(["Book Title", "Book Author", "Published Date"])
        assert result == {"title": "Book Title", "author": "Book Author", "year": "Published Date"}

    def test_missing_year(self):
        result = detect_columns(["Title", "Author"])
        assert result["title"] == "Title"
        assert result["author"] == "Author"
        assert result["year"] is None

    def test_missing_all(self):
        result = detect_columns(["Foo", "Bar", "Baz"])
        assert result == {"title": None, "author": None, "year": None}

    def test_date_keyword(self):
        result = detect_columns(["Title", "Author", "Date"])
        assert result["year"] == "Date"

    def test_published_keyword(self):
        result = detect_columns(["Title", "Author", "Year Published"])
        assert result["year"] == "Year Published"


class TestProcessCSV:
    def test_happy_path(self, tmp_path, sample_csv_content):
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"
        input_file.write_text(sample_csv_content)

        mock_client = MagicMock()
        mock_client.search_isbn.return_value = ISBNResult(
            isbn_13="9781234567890", isbn_10="1234567890", source="OpenLibrary API"
        )

        process_csv(str(input_file), str(output_file), client=mock_client)

        assert output_file.exists()
        content = output_file.read_text()
        assert "ISBN-13" in content
        assert "ISBN-10" in content
        assert "9781234567890" in content
        assert mock_client.search_isbn.call_count == 2

    def test_missing_input_file(self, tmp_path, caplog):
        import logging

        with caplog.at_level(logging.ERROR):
            process_csv(str(tmp_path / "nonexistent.csv"), str(tmp_path / "out.csv"))

        assert "not found" in caplog.text

    def test_empty_csv(self, tmp_path, caplog):
        import logging

        input_file = tmp_path / "empty.csv"
        input_file.write_text("")

        with caplog.at_level(logging.ERROR):
            process_csv(str(input_file), str(tmp_path / "out.csv"))

        assert "empty" in caplog.text

    def test_missing_title_column(self, tmp_path, caplog):
        import logging

        input_file = tmp_path / "no_title.csv"
        input_file.write_text("Author,Year\nTolkien,1937\n")

        with caplog.at_level(logging.ERROR):
            process_csv(str(input_file), str(tmp_path / "out.csv"))

        assert "title" in caplog.text.lower()

    def test_missing_author_column(self, tmp_path, sample_csv_missing_author, caplog):
        import logging

        input_file = tmp_path / "no_author.csv"
        input_file.write_text(sample_csv_missing_author)

        with caplog.at_level(logging.ERROR):
            process_csv(str(input_file), str(tmp_path / "out.csv"))

        assert "author" in caplog.text.lower()

    def test_skips_rows_with_missing_data(self, tmp_path, sample_csv_with_empty_rows):
        input_file = tmp_path / "gaps.csv"
        output_file = tmp_path / "output.csv"
        input_file.write_text(sample_csv_with_empty_rows)

        mock_client = MagicMock()
        mock_client.search_isbn.return_value = ISBNResult(
            isbn_13="9781234567890", isbn_10="", source="OpenLibrary API"
        )

        process_csv(str(input_file), str(output_file), client=mock_client)

        content = output_file.read_text()
        assert "Missing data" in content
        # Only the first row has both title and author
        assert mock_client.search_isbn.call_count == 1
