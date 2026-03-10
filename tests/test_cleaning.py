"""Tests for text cleaning and normalization."""

from ultimate_book_library.cleaning import clean_author, clean_title


class TestCleanTitle:
    def test_strips_whitespace(self):
        assert clean_title("  The Hobbit  ") == "the hobbit"

    def test_lowercases(self):
        assert clean_title("The LORD of the RINGS") == "the lord of the rings"

    def test_empty_string(self):
        assert clean_title("") == ""

    def test_already_clean(self):
        assert clean_title("clean title") == "clean title"


class TestCleanAuthor:
    def test_last_first_format(self):
        assert clean_author("Tolkien, J.R.R.") == "j.r.r. tolkien"

    def test_normal_format(self):
        assert clean_author("George Orwell") == "george orwell"

    def test_strips_whitespace(self):
        assert clean_author("  George Orwell  ") == "george orwell"

    def test_last_first_with_spaces(self):
        assert clean_author("  Tolkien ,  J.R.R.  ") == "j.r.r. tolkien"

    def test_empty_string(self):
        assert clean_author("") == ""

    def test_multiple_commas_only_splits_first(self):
        assert clean_author("Name, First, Jr.") == "first, jr. name"
