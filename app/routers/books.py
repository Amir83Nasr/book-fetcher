"""Book endpoints."""

from fastapi import APIRouter, HTTPException, Query

from app.database import execute_query
from app.db.queries import GET_ALL_BOOKS, SEARCH_BOOKS
from app.models.book import BookCreate, BookResponse, PaginatedResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=PaginatedResponse)
def list_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    """List all books."""
    offset = (page - 1) * page_size
    rows = execute_query(GET_ALL_BOOKS, (page_size, offset))

    if not rows:
        return PaginatedResponse(
            total=0, page=page, page_size=page_size, total_pages=0, results=[]
        )

    total = rows[0]["total_count"]
    results = [BookResponse(**row) for row in rows]

    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
        results=results,
    )


@router.post("", response_model=BookResponse, status_code=201)
def add_book(book: BookCreate):
    """Add a new book."""
    author_row = execute_query(
        "INSERT INTO authors (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING id",
        (book.author,),
        fetch_one=True,
    )
    author_id = author_row["id"]

    book_row = execute_query(
        "INSERT INTO books (title, author_id, year, publisher) VALUES (%s, %s, %s, %s) RETURNING id, title, year, publisher",
        (book.title, author_id, book.year, book.publisher),
        fetch_one=True,
    )

    if not book_row:
        raise HTTPException(status_code=500, detail="Failed to create book")

    book_row["author"] = book.author
    return BookResponse(**book_row)


# ========== Redis Cache ==========
@router.get("/search/redis")
def search_books_redis(
    q: str = Query(..., min_length=3, max_length=200),
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=50),
):
    """Search WITH Redis cache."""
    from app.cache import cache_key as ck
    from app.cache import get_cache_redis, set_cache_redis

    key = ck("redis", q, str(page), str(page_size))
    cached = get_cache_redis(key)
    if cached:
        return {**cached, "from_cache": True, "cache_type": "redis"}

    result = _do_search(q, page, page_size)
    set_cache_redis(key, result)
    return {**result, "from_cache": False, "cache_type": "redis"}


# ========== In-Memory Cache ==========
@router.get("/search/memory")
def search_books_memory(
    q: str = Query(..., min_length=3, max_length=200),
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=50),
):
    """Search WITH In-Memory cache."""
    from app.cache import cache_key as ck
    from app.cache import get_cache_memory, set_cache_memory

    key = ck("memory", q, str(page), str(page_size))
    cached = get_cache_memory(key)
    if cached:
        return {**cached, "from_cache": True, "cache_type": "memory"}

    result = _do_search(q, page, page_size)
    set_cache_memory(key, result)
    return {**result, "from_cache": False, "cache_type": "memory"}


# ========== No Cache ==========
@router.get("/search/nocache")
def search_books_nocache(
    q: str = Query(..., min_length=3, max_length=200),
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=50),
):
    """Search without any cache. Returns 503 if overloaded."""
    return _do_search(q, page, page_size)


# ========== Helper Function ==========


def _do_search(q: str, page: int, page_size: int) -> dict:
    """Execute search query with error handling."""
    try:
        offset = (page - 1) * page_size
        search_term = f"%{q}%"
        rows = execute_query(
            SEARCH_BOOKS, (search_term, search_term, search_term, page_size, offset)
        )
    except ConnectionError as e:
        # Connection pool exhausted or DB down
        print(f"[WARN] DB connection error: {e}")
        raise HTTPException(
            status_code=503,
            detail="Database temporarily unavailable. Please retry later.",
        )
    except Exception as e:
        print(f"[ERROR] Unexpected DB error: {e}")
        raise HTTPException(
            status_code=503, detail="Search service overloaded. Try again shortly."
        )

    if not rows:
        return {
            "query": q,
            "total": 0,
            "page": page,
            "page_size": page_size,
            "total_pages": 0,
            "results": [],
        }

    total = rows[0]["total_count"]
    results = [BookResponse(**row) for row in rows]

    return {
        "query": q,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "results": [r.model_dump() for r in results],
    }
