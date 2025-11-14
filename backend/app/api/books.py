"""
Books API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging

from app.db.database import get_db
from app.models.user import User
from app.models.book import Book, AccessLevel
from app.schemas.book import (
    BookCreate,
    BookUpdate,
    BookResponse,
    BookDetailResponse,
    BookGenerationRequest,
    BookGenerationResponse
)
from app.services.book_service import BookService
from app.middleware.auth_middleware import get_current_user, get_optional_current_user

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("", response_model=List[BookResponse])
async def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    user_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of published books

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        user_id: Filter by user ID
        db: Database session

    Returns:
        List of books
    """
    books = await BookService.get_books(
        db=db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        is_published=True
    )
    return books


@router.get("/{book_id}", response_model=BookDetailResponse)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get a book by ID

    Args:
        book_id: Book ID
        db: Database session
        current_user: Current user (optional)

    Returns:
        Book details

    Raises:
        HTTPException: If book not found or access denied
    """
    book = await BookService.get_book(db, book_id, include_chapters=True)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # Check access permissions
    if book.is_blocked and (not current_user or current_user.id != book.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This book has been blocked"
        )

    if not book.is_published and (not current_user or current_user.id != book.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This book is not published"
        )

    # Check access level
    if book.access_level == AccessLevel.REGISTERED and not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This book requires authentication"
        )

    # Increment views
    await BookService.increment_views(db, book_id)

    return book


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new book

    Args:
        book_data: Book creation data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Created book
    """
    book = await BookService.create_book(db, book_data, current_user.id)
    return book


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a book

    Args:
        book_id: Book ID
        book_data: Book update data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Updated book

    Raises:
        HTTPException: If book not found or access denied
    """
    book = await BookService.get_book(db, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    if book.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this book"
        )

    updated_book = await BookService.update_book(db, book_id, book_data)
    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a book

    Args:
        book_id: Book ID
        db: Database session
        current_user: Current authenticated user

    Raises:
        HTTPException: If book not found or access denied
    """
    book = await BookService.get_book(db, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    if book.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this book"
        )

    await BookService.delete_book(db, book_id)


@router.post("/{book_id}/publish", response_model=BookResponse)
async def publish_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Publish a book

    Args:
        book_id: Book ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Published book

    Raises:
        HTTPException: If book not found or access denied
    """
    book = await BookService.get_book(db, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    if book.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to publish this book"
        )

    published_book = await BookService.publish_book(db, book_id)
    return published_book


@router.post("/generate", response_model=BookGenerationResponse)
async def generate_book(
    generation_request: BookGenerationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate a book using AI

    Args:
        generation_request: Generation request data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Generated book information

    Raises:
        HTTPException: If generation fails or user has no generations left
    """
    # TODO: Check user's generation limit from subscription

    try:
        book = await BookService.generate_book(db, current_user.id, generation_request)

        return BookGenerationResponse(
            book_id=book.id,
            title=book.title,
            description=book.description or "",
            status="success",
            message="Book generated successfully"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error generating book: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate book"
        )


# Like endpoints
@router.post("/{book_id}/like", status_code=status.HTTP_201_CREATED)
async def like_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Like a book"""
    from app.models.like import Like
    from sqlalchemy import select

    # Check if book exists
    book = await BookService.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    # Check if already liked
    result = await db.execute(
        select(Like).where(Like.user_id == current_user.id, Like.book_id == book_id)
    )
    existing_like = result.scalar_one_or_none()

    if existing_like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already liked")

    # Create like
    like = Like(user_id=current_user.id, book_id=book_id)
    db.add(like)
    book.likes_count += 1
    await db.commit()

    return {"message": "Book liked successfully", "likes_count": book.likes_count}


@router.delete("/{book_id}/like", status_code=status.HTTP_200_OK)
async def unlike_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Unlike a book"""
    from app.models.like import Like
    from sqlalchemy import select

    # Check if book exists
    book = await BookService.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    # Check if liked
    result = await db.execute(
        select(Like).where(Like.user_id == current_user.id, Like.book_id == book_id)
    )
    like = result.scalar_one_or_none()

    if not like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not liked yet")

    # Remove like
    await db.delete(like)
    if book.likes_count > 0:
        book.likes_count -= 1
    await db.commit()

    return {"message": "Book unliked successfully", "likes_count": book.likes_count}


@router.get("/{book_id}/liked", status_code=status.HTTP_200_OK)
async def check_if_liked(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check if current user liked the book"""
    from app.models.like import Like
    from sqlalchemy import select

    result = await db.execute(
        select(Like).where(Like.user_id == current_user.id, Like.book_id == book_id)
    )
    like = result.scalar_one_or_none()

    return {"liked": like is not None}

# Export endpoints
from fastapi.responses import Response
from app.services.export_service import export_service

@router.get("/{book_id}/export/pdf")
async def export_book_to_pdf(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export book to PDF"""
    book = await BookService.get_book(db, book_id, include_chapters=True)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    # Prepare book data
    book_data = {
        "title": book.title,
        "description": book.description,
        "chapters": [
            {
                "number": chapter.chapter_number,
                "title": chapter.title,
                "blocks": [
                    {"block_type": block.block_type.value, "content": block.content}
                    for block in chapter.blocks
                ]
            }
            for chapter in book.chapters
        ]
    }

    pdf_bytes = export_service.export_to_pdf(book_data)
    return Response(content=pdf_bytes, media_type="application/pdf",
                    headers={"Content-Disposition": f"attachment; filename={book.title}.pdf"})


@router.get("/{book_id}/export/epub")
async def export_book_to_epub(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export book to ePub"""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                        detail="ePub export coming soon")
