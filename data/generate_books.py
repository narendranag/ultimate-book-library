#!/usr/bin/env python3
"""Generate the 10,000-book seed dataset.

Reads batch JSON files from data/batches/ and merges them,
deduplicates by ISBN, validates, and writes the final books.json.

Run: python data/generate_books.py
"""

import json
import sys
from pathlib import Path


def load_batches(batch_dir: Path) -> list[dict]:
    """Load all batch JSON files and combine."""
    books = []
    for f in sorted(batch_dir.glob("batch_*.json")):
        print(f"  Loading {f.name}...")
        with open(f) as fh:
            batch = json.load(fh)
            print(f"    {len(batch)} books")
            books.extend(batch)
    return books


def deduplicate(books: list[dict]) -> list[dict]:
    """Remove duplicates by ISBN-13, keeping first occurrence."""
    seen_isbns = set()
    seen_titles = set()
    unique = []
    for book in books:
        isbn = book.get("isbn_13", "")
        title_key = (book["title"].lower(), tuple(a.lower() for a in book["authors"]))

        if isbn and isbn in seen_isbns:
            continue
        if title_key in seen_titles:
            continue

        if isbn:
            seen_isbns.add(isbn)
        seen_titles.add(title_key)
        unique.append(book)
    return unique


def add_defaults(books: list[dict]) -> list[dict]:
    """Ensure all books have required fields with defaults."""
    for book in books:
        book.setdefault("language", "en")
        book.setdefault("genres", [])
        book.setdefault("source", "seed")
        # Remove None values
        book = {k: v for k, v in book.items() if v is not None}
    return books


def validate(books: list[dict]) -> None:
    """Basic validation."""
    errors = 0
    for i, book in enumerate(books):
        if not book.get("title"):
            print(f"  ERROR: Book {i} missing title")
            errors += 1
        if not book.get("authors"):
            print(f"  ERROR: Book {i} '{book.get('title', '?')}' missing authors")
            errors += 1
    if errors:
        print(f"\n  {errors} validation errors found!")
        sys.exit(1)


def main():
    data_dir = Path(__file__).parent
    batch_dir = data_dir / "batches"

    print("Loading batches...")
    books = load_batches(batch_dir)
    print(f"\nTotal raw: {len(books)} books")

    print("\nDeduplicating...")
    books = deduplicate(books)
    print(f"After dedup: {len(books)} books")

    print("\nAdding defaults...")
    books = add_defaults(books)

    print("\nValidating...")
    validate(books)

    # Sort by title
    books.sort(key=lambda b: b["title"].lower())

    output = {"version": "1.0", "books": books}
    out_path = data_dir / "books.json"

    print(f"\nWriting {len(books)} books to {out_path}...")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("Done!")

    # Stats
    genres = {}
    languages = {}
    for book in books:
        for g in book.get("genres", []):
            genres[g] = genres.get(g, 0) + 1
        lang = book.get("language", "en")
        languages[lang] = languages.get(lang, 0) + 1

    print(f"\nGenre distribution:")
    for g, c in sorted(genres.items(), key=lambda x: -x[1])[:20]:
        print(f"  {g}: {c}")

    print(f"\nLanguage distribution:")
    for l, c in sorted(languages.items(), key=lambda x: -x[1]):
        print(f"  {l}: {c}")


if __name__ == "__main__":
    main()
