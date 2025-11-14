"""
Admin API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.db.database import get_db
from app.models.user import User, UserRole
from app.models.book import Book
from app.middleware.auth_middleware import get_current_admin_user

router = APIRouter()

@router.get("/stats")
async def get_admin_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get platform statistics"""
    users_count = await db.scalar(select(func.count()).select_from(User))
    books_count = await db.scalar(select(func.count()).select_from(Book))
    published_books = await db.scalar(select(func.count()).select_from(Book).where(Book.is_published == True))
    return {"users": users_count, "books": books_count, "published_books": published_books}

@router.get("/users")
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get all users (admin only)"""
    result = await db.execute(select(User).order_by(User.created_at.desc()).limit(100))
    users = result.scalars().all()
    return [{"id": u.id, "username": u.username, "email": u.email, "role": u.role.value} for u in users]

@router.post("/users/{user_id}/block")
async def block_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Block a user"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_blocked = True
    await db.commit()
    return {"message": "User blocked"}

@router.post("/books/{book_id}/block")
async def block_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Block a book"""
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    book.is_blocked = True
    await db.commit()
    return {"message": "Book blocked"}
