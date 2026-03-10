"""Shared test fixtures."""

import pytest


@pytest.fixture
def openlibrary_response_both_isbns():
    """A realistic Open Library response with both ISBN-13 and ISBN-10."""
    return {
        "numFound": 1,
        "docs": [
            {
                "title": "The Lord of the Rings",
                "author_name": ["J.R.R. Tolkien"],
                "isbn": ["9780618640157", "0618640150", "9780261103252"],
            }
        ],
    }


@pytest.fixture
def openlibrary_response_isbn13_only():
    """A response with only ISBN-13."""
    return {
        "numFound": 1,
        "docs": [
            {
                "title": "Some Book",
                "author_name": ["Some Author"],
                "isbn": ["9781234567890"],
            }
        ],
    }


@pytest.fixture
def openlibrary_response_no_isbn():
    """A response where books have no ISBN field."""
    return {
        "numFound": 1,
        "docs": [
            {
                "title": "Old Book",
                "author_name": ["Old Author"],
            }
        ],
    }


@pytest.fixture
def openlibrary_response_not_found():
    """A response with no results."""
    return {"numFound": 0, "docs": []}


@pytest.fixture
def sample_csv_content():
    """Sample CSV content for testing."""
    return "Title,Author,Year\nThe Hobbit,Tolkien J.R.R.,1937\n1984,Orwell George,1949\n"


@pytest.fixture
def sample_csv_missing_author():
    """CSV content missing the author column."""
    return "Title,Year\nThe Hobbit,1937\n"


@pytest.fixture
def sample_csv_with_empty_rows():
    """CSV with rows missing title or author values."""
    return (
        "Title,Author,Year\n"
        "The Hobbit,Tolkien J.R.R.,1937\n"
        ",Missing Author,2000\n"
        "Missing Title,,1999\n"
    )


@pytest.fixture
def tmp_csv_file(tmp_path, sample_csv_content):
    """Write sample CSV to a temporary file."""
    csv_file = tmp_path / "input.csv"
    csv_file.write_text(sample_csv_content)
    return csv_file
