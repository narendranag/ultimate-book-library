"""Tests for the CLI entry point."""

import subprocess
import sys


class TestCLI:
    def test_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "ultimate_book_library", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "find-isbn" in result.stdout

    def test_no_command_shows_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "ultimate_book_library"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "find-isbn" in result.stdout

    def test_find_isbn_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "ultimate_book_library", "find-isbn", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "input_file" in result.stdout
        assert "--rate-limit" in result.stdout
        assert "--verbose" in result.stdout

    def test_find_isbn_missing_args(self):
        result = subprocess.run(
            [sys.executable, "-m", "ultimate_book_library", "find-isbn"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
