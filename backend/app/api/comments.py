"""
Comments API endpoints (FULL IMPLEMENTATION)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
import logging

from app.db.database import get_db
from app.models.user import User
from app.models.comment import Comment, CommentStatus
from app.models.book import Book
from app.middleware.auth_middleware import get_current_user
from pydantic import BaseModel

router = APIRouter()
logger = logging.getLogger(__name__)


# Schemas
class CommentCreate(BaseModel):
    content: str
    parent_comment_id: Optional[int] = None


class CommentResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    parent_comment_id: Optional[int]
    content: str
    status: str
    created_at: str
    updated_at: str
    username: str

    class Config:
        from_attributes = True


@router.get("/book/{book_id}", response_model=List[CommentResponse])
async def get_book_comments(
    book_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get comments for a book"""
    book_result = await db.execute(select(Book).where(Book.id == book_id))
    book = book_result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    query = select(Comment).where(
        and_(Comment.book_id == book_id, Comment.status == CommentStatus.APPROVED)
    ).order_by(Comment.created_at.desc()).offset(skip).limit(limit)

    result = await db.execute(query)
    comments = result.scalars().all()

    comment_responses = []
    for comment in comments:
        user_result = await db.execute(select(User).where(User.id == comment.user_id))
        user = user_result.scalar_one_or_none()
        comment_responses.append(CommentResponse(
            id=comment.id,
            user_id=comment.user_id,
            book_id=comment.book_id,
            parent_comment_id=comment.parent_comment_id,
            content=comment.content,
            status=comment.status.value,
            created_at=str(comment.created_at),
            updated_at=str(comment.updated_at),
            username=user.username if user else "Unknown"
        ))

    return comment_responses


@router.post("/book/{book_id}", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    book_id: int,
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new comment"""
    book_result = await db.execute(select(Book).where(Book.id == book_id))
    book = book_result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    comment = Comment(
        user_id=current_user.id,
        book_id=book_id,
        parent_comment_id=comment_data.parent_comment_id,
        content=comment_data.content,
        status=CommentStatus.APPROVED
    )
    db.add(comment)
    book.comments_count += 1
    await db.commit()
    await db.refresh(comment)

    return CommentResponse(
        id=comment.id,
        user_id=comment.user_id,
        book_id=comment.book_id,
        parent_comment_id=comment.parent_comment_id,
        content=comment.content,
        status=comment.status.value,
        created_at=str(comment.created_at),
        updated_at=str(comment.updated_at),
        username=current_user.username
    )


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a comment"""
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    from app.models.user import UserRole
    if comment.user_id != current_user.id and current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    book_result = await db.execute(select(Book).where(Book.id == comment.book_id))
    book = book_result.scalar_one_or_none()
    if book and book.comments_count > 0:
        book.comments_count -= 1

    await db.delete(comment)
    await db.commit()
