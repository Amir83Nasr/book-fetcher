"""Tests for the API module."""

from book_fetcher.api import fetch_books


def test_fetch_books_returns_list():
    books = fetch_books(limit=2, subject="fiction", min_year=2000)
    assert isinstance(books, list)
    # Check that returned books have expected keys (at least some)
    for book in books:
        assert "title" in book
