"""Author endpoints."""

from fastapi import APIRouter, Query

from app.cache import cache_key, get_cache, set_cache
from app.database import execute_query
from app.db.queries import SEARCH_AUTHORS
from app.models.author import AuthorWithBookCount

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/search")
def search_authors(
    q: str = Query(..., min_length=3, max_length=100, description="Search authors"),
):
    """Search authors and return their book count. Results are cached."""
    ck = cache_key("authors", q)

    # Check cache first
    cached = get_cache(ck)
    if cached:
        cached["from_cache"] = True
        return cached

    # Cache miss - query database
    rows = execute_query(SEARCH_AUTHORS, (f"%{q}%",))
    results = [AuthorWithBookCount(**row) for row in rows]

    response = {
        "query": q,
        "results": [r.model_dump() for r in results],
        "from_cache": False,
    }

    # Store in cache
    cache_data = {**response, "from_cache": False}
    set_cache(ck, cache_data)

    return response
