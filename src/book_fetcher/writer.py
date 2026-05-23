"""Save book data to CSV."""

import csv
from pathlib import Path
from typing import Any

CSV_FIELDNAMES = ["title", "author", "year"]


def extract_book_info(book: dict[str, Any]) -> dict[str, str]:
    """Extract and clean a single book's data for CSV output."""
    title = book.get("title", "Unknown")
    authors = book.get("author_name", [])
    author_str = ", ".join(authors) if authors else "Unknown"
    year = str(book.get("first_publish_year", ""))
    return {
        "title": title,
        "author": author_str,
        "year": year,
    }


def save_to_csv(books: list[dict[str, Any]], output_path: Path) -> None:
    """Write filtered books to a CSV file, creating directory if needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for book in books:
            writer.writerow(extract_book_info(book))
    print(f"Saved {len(books)} books to {output_path}")
