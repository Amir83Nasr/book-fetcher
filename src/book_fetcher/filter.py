"""Filter books based on publish year."""

from typing import Any


def filter_books_by_year(
    books: list[dict[str, Any]], min_year: int
) -> list[dict[str, Any]]:
    """Filter books with valid first_publish_year > min_year, sorted by year."""
    filtered = []
    for book in books:
        year = book.get("first_publish_year")
        if year is not None and year > min_year:
            filtered.append(book)
    filtered.sort(key=lambda x: x.get("first_publish_year", 0))
    return filtered
