"""Command-line interface for the Ultimate Book Library."""

import csv
import json
import logging
from collections import Counter
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from ultimate_book_library.database import DEFAULT_DATA_PATH, build_database, load_library
from ultimate_book_library.schema import BookEntry, BookLibrary
from ultimate_book_library.validation import validate_library

app = typer.Typer(
    name="booklib",
    help="Ultimate Book Library - tools to find, enrich, and manage book data.",
    no_args_is_help=True,
)

console = Console()
err_console = Console(stderr=True)


def _configure_logging(verbose: bool) -> None:
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format="%(message)s")


def _load_or_exit(data: Path | None) -> BookLibrary:
    """Load library data or exit with error."""
    try:
        return load_library(data)
    except FileNotFoundError as e:
        err_console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e


# -- find-isbn command (preserved from Phase 1) --


@app.command()
def find_isbn(
    input_file: Annotated[str, typer.Argument(help="Input CSV file with books")],
    output_file: Annotated[str, typer.Argument(help="Output CSV file to write results")],
    rate_limit: Annotated[float, typer.Option(help="Seconds between API requests")] = 1.0,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose output")] = False,
) -> None:
    """Find ISBNs for books in a CSV file using the Open Library API."""
    _configure_logging(verbose)

    from ultimate_book_library.isbn_lookup import process_csv
    from ultimate_book_library.openlibrary import OpenLibraryClient

    client = OpenLibraryClient(rate_limit_seconds=rate_limit)
    process_csv(input_file, output_file, client=client)
    console.print(f"[green]Done![/green] Results written to {output_file}")


# -- build-db command --


@app.command()
def build_db(
    data: Annotated[Path | None, typer.Option(help="Path to books.json")] = None,
    output: Annotated[
        Path | None, typer.Option("--output", "-o", help="Output database path")
    ] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose output")] = False,
) -> None:
    """Build SQLite database from book data."""
    _configure_logging(verbose)
    library = _load_or_exit(data)

    try:
        result_path = build_database(library, output)
        console.print(f"[green]Database built:[/green] {result_path}")
        console.print(f"  {len(library.books)} books loaded")
    except Exception as e:
        err_console.print(f"[red]Error building database:[/red] {e}")
        raise typer.Exit(1) from e


# -- validate command --


@app.command()
def validate(
    data: Annotated[Path | None, typer.Option(help="Path to books.json")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose output")] = False,
) -> None:
    """Validate book library data for issues."""
    _configure_logging(verbose)
    library = _load_or_exit(data)
    issues = validate_library(library)

    console.print(f"Validated [bold]{len(library.books)}[/bold] books")
    if issues:
        console.print(f"\n[yellow]Found {len(issues)} issue(s):[/yellow]")
        for issue in issues:
            console.print(f"  [yellow]-[/yellow] {issue}")
        raise typer.Exit(1)
    else:
        console.print("[green]No issues found![/green]")


# -- list command --


@app.command(name="list")
def list_books(
    data: Annotated[Path | None, typer.Option(help="Path to books.json")] = None,
    genre: Annotated[str | None, typer.Option(help="Filter by genre")] = None,
    language: Annotated[str | None, typer.Option(help="Filter by language code")] = None,
    limit: Annotated[int, typer.Option(help="Max books to show")] = 20,
) -> None:
    """List books in the library."""
    library = _load_or_exit(data)
    books = library.books

    if genre:
        genre_lower = genre.lower()
        books = [b for b in books if any(genre_lower in g.lower() for g in b.genres)]

    if language:
        books = [b for b in books if b.language == language]

    if not books:
        console.print("[yellow]No books match the filters.[/yellow]")
        return

    table = Table(title=f"Books ({len(books)} total, showing up to {limit})")
    table.add_column("Title", style="bold")
    table.add_column("Authors")
    table.add_column("Year", justify="right")
    table.add_column("Genres")
    table.add_column("Lang", justify="center")
    table.add_column("Pages", justify="right")

    for book in books[:limit]:
        table.add_row(
            book.title,
            ", ".join(book.authors),
            str(book.year_published) if book.year_published else "-",
            ", ".join(book.genres[:3]),
            book.language,
            str(book.page_count) if book.page_count else "-",
        )

    console.print(table)


# -- search command --


@app.command()
def search(
    query: Annotated[str, typer.Argument(help="Search query")],
    data: Annotated[Path | None, typer.Option(help="Path to books.json")] = None,
    field: Annotated[
        str | None, typer.Option(help="Limit search to field: title, author, genre")
    ] = None,
) -> None:
    """Search books by title, author, or genre."""
    library = _load_or_exit(data)
    query_lower = query.lower()
    results: list[BookEntry] = []

    for book in library.books:
        if field == "title":
            match = query_lower in book.title.lower()
        elif field == "author":
            match = any(query_lower in a.lower() for a in book.authors)
        elif field == "genre":
            match = any(query_lower in g.lower() for g in book.genres)
        else:
            match = (
                query_lower in book.title.lower()
                or any(query_lower in a.lower() for a in book.authors)
                or any(query_lower in g.lower() for g in book.genres)
            )

        if match:
            results.append(book)

    if not results:
        console.print(f"[yellow]No books found matching '{query}'[/yellow]")
        return

    table = Table(title=f"Search results for '{query}' ({len(results)} found)")
    table.add_column("Title", style="bold")
    table.add_column("Authors")
    table.add_column("Year", justify="right")
    table.add_column("ISBN-13")
    table.add_column("Genres")

    for book in results:
        table.add_row(
            book.title,
            ", ".join(book.authors),
            str(book.year_published) if book.year_published else "-",
            book.isbn_13 or "-",
            ", ".join(book.genres[:3]),
        )

    console.print(table)


# -- add command --


@app.command()
def add(
    title: Annotated[str, typer.Argument(help="Book title")],
    author: Annotated[list[str], typer.Option("--author", "-a", help="Author name(s)")],
    year: Annotated[int | None, typer.Option(help="Publication year")] = None,
    isbn_13: Annotated[str | None, typer.Option(help="ISBN-13")] = None,
    isbn_10: Annotated[str | None, typer.Option(help="ISBN-10")] = None,
    genre: Annotated[list[str] | None, typer.Option("--genre", "-g", help="Genre(s)")] = None,
    language: Annotated[str, typer.Option(help="Language code")] = "en",
    data: Annotated[Path | None, typer.Option(help="Path to books.json")] = None,
) -> None:
    """Add a book to the library."""
    data_path = data or DEFAULT_DATA_PATH

    # Load existing library
    try:
        library = load_library(data_path)
    except FileNotFoundError:
        library = BookLibrary(books=[])

    new_book = BookEntry(
        title=title,
        authors=author,
        year_published=year,
        isbn_13=isbn_13,
        isbn_10=isbn_10,
        genres=genre or [],
        language=language,
    )

    library.books.append(new_book)

    # Write back
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(library.model_dump(mode="json"), f, indent=2, default=str)
        f.write("\n")

    console.print(f"[green]Added:[/green] {title} by {', '.join(author)}")
    console.print(f"  Library now has {len(library.books)} books")


# -- stats command --


@app.command()
def stats(
    data: Annotated[Path | None, typer.Option(help="Path to books.json")] = None,
) -> None:
    """Show collection statistics."""
    library = _load_or_exit(data)
    books = library.books

    console.print("\n[bold]Library Statistics[/bold]")
    console.print(f"  Total books: [bold]{len(books)}[/bold]")

    # Year range
    years = [b.year_published for b in books if b.year_published is not None]
    if years:
        console.print(f"  Year range: {min(years)} - {max(years)}")

    # Pages
    pages = [b.page_count for b in books if b.page_count]
    if pages:
        console.print(f"  Total pages: {sum(pages):,}")
        console.print(f"  Average pages: {sum(pages) // len(pages):,}")

    # Genre breakdown
    genre_counter: Counter[str] = Counter()
    for book in books:
        for g in book.genres:
            genre_counter[g] += 1

    if genre_counter:
        console.print("\n[bold]Top Genres[/bold]")
        genre_table = Table(show_header=True)
        genre_table.add_column("Genre")
        genre_table.add_column("Count", justify="right")
        for genre_name, count in genre_counter.most_common(10):
            genre_table.add_row(genre_name, str(count))
        console.print(genre_table)

    # Language breakdown
    lang_counter: Counter[str] = Counter()
    for book in books:
        lang_counter[book.language] += 1

    if lang_counter:
        console.print("\n[bold]Languages[/bold]")
        lang_table = Table(show_header=True)
        lang_table.add_column("Language")
        lang_table.add_column("Count", justify="right")
        for lang, count in lang_counter.most_common():
            lang_table.add_row(lang, str(count))
        console.print(lang_table)

    # ISBN coverage
    with_isbn = sum(1 for b in books if b.isbn_13 or b.isbn_10)
    console.print(f"\n  ISBN coverage: {with_isbn}/{len(books)} ({100 * with_isbn // len(books)}%)")


# -- serve command --


@app.command()
def serve(
    data: Annotated[Path | None, typer.Option(help="Path to books.json")] = None,
    host: Annotated[str, typer.Option(help="Host to bind to")] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Port to bind to")] = 8000,
) -> None:
    """Start the REST API server."""
    try:
        import uvicorn

        from ultimate_book_library.api.app import create_app
    except ImportError:
        err_console.print(
            "[red]API dependencies not installed.[/red] "
            "Install with: pip install 'ultimate-book-library[api]'"
        )
        raise typer.Exit(1) from None

    api_app = create_app(data_path=data)
    console.print(f"Starting API server at [bold]http://{host}:{port}[/bold]")
    console.print(f"  API docs: [link]http://{host}:{port}/docs[/link]")
    uvicorn.run(api_app, host=host, port=port)


# -- export command --


@app.command()
def export(
    output: Annotated[str, typer.Argument(help="Output file path")],
    fmt: Annotated[
        str, typer.Option("--format", "-f", help="Output format: csv, json, markdown")
    ] = "csv",
    data: Annotated[Path | None, typer.Option(help="Path to books.json")] = None,
) -> None:
    """Export the book library to CSV, JSON, or Markdown."""
    library = _load_or_exit(data)

    if fmt == "csv":
        _export_csv(library, output)
    elif fmt == "json":
        _export_json(library, output)
    elif fmt == "markdown":
        _export_markdown(library, output)
    else:
        err_console.print(f"[red]Unknown format:[/red] {fmt}. Use csv, json, or markdown.")
        raise typer.Exit(1)

    console.print(f"[green]Exported {len(library.books)} books to {output}[/green] (format: {fmt})")


def _export_csv(library: BookLibrary, output: str) -> None:
    fieldnames = [
        "Title",
        "Authors",
        "Year",
        "ISBN-13",
        "ISBN-10",
        "Genres",
        "Language",
        "Pages",
    ]
    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for book in library.books:
            writer.writerow(
                {
                    "Title": book.title,
                    "Authors": "; ".join(book.authors),
                    "Year": book.year_published or "",
                    "ISBN-13": book.isbn_13 or "",
                    "ISBN-10": book.isbn_10 or "",
                    "Genres": "; ".join(book.genres),
                    "Language": book.language,
                    "Pages": book.page_count or "",
                }
            )


def _export_json(library: BookLibrary, output: str) -> None:
    with open(output, "w", encoding="utf-8") as f:
        json.dump(
            [book.model_dump(mode="json", exclude_none=True) for book in library.books],
            f,
            indent=2,
            default=str,
        )
        f.write("\n")


def _export_markdown(library: BookLibrary, output: str) -> None:
    lines = [
        "| Title | Authors | Year | ISBN-13 | Genres |",
        "|-------|---------|------|---------|--------|",
    ]
    for book in library.books:
        lines.append(
            f"| {book.title} "
            f"| {', '.join(book.authors)} "
            f"| {book.year_published or '-'} "
            f"| {book.isbn_13 or '-'} "
            f"| {', '.join(book.genres[:3])} |"
        )
    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        f.write("\n")
