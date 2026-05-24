"""FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import authors, books

app = FastAPI(
    title="Book API",
    description="A book search API with PostgreSQL and Redis caching",
    version="1.0.0",
)

# CORS (allow frontend to call API from different origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(books.router)
app.include_router(authors.router)


@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "Book API"}


@app.get("/cache/clear", tags=["Admin"])
def clear_cache():
    """Clear all cache. Useful for testing."""
    from app.cache import delete_cache

    delete_cache()
    return {"message": "Cache cleared"}
