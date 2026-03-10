"""Text cleaning and normalization for book metadata."""


def clean_title(title: str) -> str:
    """Clean and normalize a book title for better search results."""
    return title.strip().lower()


def clean_author(author: str) -> str:
    """Clean and normalize an author name for better search results.

    Handles "Last, First" format by converting to "First Last".
    """
    if "," in author:
        parts = author.split(",", 1)
        return f"{parts[1].strip()} {parts[0].strip()}".lower()
    return author.strip().lower()
