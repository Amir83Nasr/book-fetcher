"""Author Pydantic models."""

from pydantic import BaseModel


class AuthorWithBookCount(BaseModel):
    """Author with their book count."""

    name: str
    book_count: int
