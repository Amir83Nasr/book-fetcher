"""Command-line interface for the book fetcher."""

import sys
from pathlib import Path

from book_fetcher.api import fetch_books
from book_fetcher.filter import filter_books_by_year
from book_fetcher.writer import save_to_csv

# Configuration constants (in a future you can move to a config module or env vars)
BOOK_LIMIT = 50
BOOK_YEAR = 2000
BOOK_SUBJECT = "fiction"
OUTPUT_PATH = Path("data") / "books_after_2000.csv"


def main() -> None:
    """Main entry point."""
    print(f"Fetching {BOOK_LIMIT} books about '{BOOK_SUBJECT}'...")
    books = fetch_books(BOOK_LIMIT, BOOK_SUBJECT, BOOK_YEAR)
    print(f"Received {len(books)} books from API.")

    filtered = filter_books_by_year(books, BOOK_YEAR)
    if not filtered:
        print("No books matched the year filter.", file=sys.stderr)
        sys.exit(0)

    save_to_csv(filtered, OUTPUT_PATH)


if __name__ == "__main__":
    main()
