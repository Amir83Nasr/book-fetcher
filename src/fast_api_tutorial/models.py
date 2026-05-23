from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    author: str = Field(..., min_length=3, max_length=100)
    year: int = Field(..., ge=1000, le=2026)
