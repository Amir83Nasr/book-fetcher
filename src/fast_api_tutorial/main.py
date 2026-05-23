from fastapi import FastAPI, Query

from .db import books_db
from .models import Book

app = FastAPI(title="Book Search API", version="1.0.0")


books: list[Book] = books_db


@app.get("/search")
def search_books(
    q: str = Query(..., min_length=3, max_length=100),
) -> dict[str, str | int | list[Book]]:
    """Search books."""
    q_lower = q.lower()
    results = [
        book
        for book in books
        if q_lower in book.title.lower() or q_lower in book.author.lower()
    ]
    return {"query": q, "total": len(results), "results": results}


@app.post("/books", status_code=201)
def add_book(book: Book) -> dict[str, str | Book]:
    """
    Add a new book to the collection.
    """
    books.append(book)
    return {"message": "Book added successfully", "book": book}


@app.get("/books")
def list_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
) -> dict[str, int | list[Book]]:
    """
    List all books, optionally filtered by search query.
    """
    sorted_books = books

    total = len(sorted_books)
    start = (page - 1) * page_size
    end = start + page_size
    paged_results = sorted_books[start:end]

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "results": paged_results,
    }
