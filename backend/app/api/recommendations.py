"""
Recommendations API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.db.database import get_db
from app.models.user import User
from app.models.book import Book
from app.models.like import Like
from app.middleware.auth_middleware import get_current_user

router = APIRouter()

@router.get("")
async def get_recommendations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get personalized book recommendations"""
    # Simple recommendation: most liked books
    result = await db.execute(
        select(Book).where(Book.is_published == True, Book.is_blocked == False)
        .order_by(Book.likes_count.desc()).limit(10)
    )
    books = result.scalars().all()
    return [{"id": b.id, "title": b.title, "likes": b.likes_count} for b in books]
