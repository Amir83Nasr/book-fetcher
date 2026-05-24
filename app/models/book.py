"""Book Pydantic models."""

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    """Model for creating a new book."""

    title: str = Field(..., min_length=3, max_length=200)
    author: str = Field(..., min_length=3, max_length=100)
    year: int = Field(..., ge=1000, le=2026)
    publisher: str = Field(..., min_length=3, max_length=100)


class BookResponse(BaseModel):
    """Model for book response."""

    id: int
    title: str
    author: str
    year: int
    publisher: str


class PaginatedResponse(BaseModel):
    """Generic paginated response."""

    total: int
    page: int
    page_size: int
    total_pages: int
    results: list
