"""
Book schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.book import AccessLevel


class ChapterBase(BaseModel):
    """Base chapter schema"""
    chapter_number: int
    title: Optional[str] = None


class ChapterCreate(ChapterBase):
    """Chapter creation schema"""
    pass


class ChapterResponse(ChapterBase):
    """Chapter response schema"""
    id: int
    book_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BlockBase(BaseModel):
    """Base block schema"""
    block_type: str
    content: Optional[str] = None
    order_index: int


class BlockCreate(BlockBase):
    """Block creation schema"""
    chapter_id: int


class BlockUpdate(BaseModel):
    """Block update schema"""
    content: Optional[str] = None
    order_index: Optional[int] = None


class BlockResponse(BlockBase):
    """Block response schema"""
    id: int
    chapter_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    """Base book schema"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    language: str = "ru"
    age_group: Optional[str] = None


class BookCreate(BookBase):
    """Book creation schema"""
    cover_url: Optional[str] = None
    access_level: AccessLevel = AccessLevel.PUBLIC


class BookUpdate(BaseModel):
    """Book update schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    cover_url: Optional[str] = None
    language: Optional[str] = None
    age_group: Optional[str] = None
    access_level: Optional[AccessLevel] = None
    premium_tier_rating: Optional[int] = None


class BookResponse(BookBase):
    """Book response schema"""
    id: int
    user_id: int
    cover_url: Optional[str] = None
    access_level: AccessLevel
    premium_tier_rating: Optional[int] = None
    views_count: int
    likes_count: int
    comments_count: int
    average_reading_time: Optional[int] = None
    created_at: datetime
    published_at: Optional[datetime] = None
    updated_at: datetime
    is_published: bool
    is_blocked: bool
    block_reason: Optional[str] = None

    class Config:
        from_attributes = True


class BookDetailResponse(BookResponse):
    """Detailed book response with chapters"""
    chapters: List[ChapterResponse] = []


class BookGenerationRequest(BaseModel):
    """Book generation request schema"""
    plot: str = Field(..., min_length=10, max_length=2000)
    language: str = "ru"
    age_group: str = "7-12"
    pages: int = Field(10, ge=1, le=20)
    style: str = "сказка"
    system_prompt: Optional[str] = None


class BookGenerationResponse(BaseModel):
    """Book generation response schema"""
    book_id: int
    title: str
    description: str
    status: str
    message: str
