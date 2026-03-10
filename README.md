# Ultimate Book Library

[![CI](https://github.com/narendranag/ultimate-book-library/actions/workflows/ci.yml/badge.svg)](https://github.com/narendranag/ultimate-book-library/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A curated collection of the best books in the world, with tools to find, enrich, and manage book data.

## Quick Start

```bash
# Install
uv tool install ultimate-book-library

# Look up ISBNs for books in a CSV
booklib find-isbn books.csv books_with_isbns.csv
```

## Installation

### With uv (recommended)

```bash
uv tool install ultimate-book-library
```

### With pip

```bash
pip install .
```

### From source

```bash
git clone https://github.com/narendranag/ultimate-book-library.git
cd ultimate-book-library
uv sync
```

## Usage

### Find ISBNs

Look up ISBN-13 and ISBN-10 for books in a CSV file using the Open Library API:

```bash
booklib find-isbn input.csv output.csv
```

Your input CSV should have columns for title and author (detected automatically). An optional year/date column improves accuracy.

**Options:**

```
--rate-limit FLOAT    Seconds between API requests (default: 1.0)
--verbose, -v         Enable verbose output
```

**Example input CSV:**

```csv
Title,Author,Year
The Hobbit,"Tolkien, J.R.R.",1937
1984,George Orwell,1949
```

## Development

### Setup

```bash
git clone https://github.com/narendranag/ultimate-book-library.git
cd ultimate-book-library
uv sync --dev
```

### Run tests

```bash
uv run pytest
uv run pytest --cov=ultimate_book_library   # with coverage
```

### Linting

```bash
uv run ruff check src/ tests/
uv run ruff format src/ tests/
```

### Pre-commit hooks

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## Roadmap

- **Phase 1** (current): Foundation and tooling - proper packaging, tests, CI/CD
- **Phase 2**: Data layer - curated book list, schema, SQLite database
- **Phase 3**: CLI enhancement - Typer-based CLI with search, enrich, export commands
- **Phase 4**: API service - FastAPI REST API with OpenAPI docs
- **Phase 5**: Web frontend - HTMX-powered book browsing UI

## License

MIT
