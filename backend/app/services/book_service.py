"""
Book service
"""
import logging
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from datetime import datetime

from app.models.book import Book, AccessLevel
from app.models.chapter import Chapter
from app.models.block import Block, BlockType
from app.models.user import User
from app.schemas.book import BookCreate, BookUpdate, BookGenerationRequest
from app.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)


class BookService:
    """Service for book operations"""

    @staticmethod
    async def create_book(db: AsyncSession, book_data: BookCreate, user_id: int) -> Book:
        """
        Create a new book

        Args:
            db: Database session
            book_data: Book creation data
            user_id: User ID

        Returns:
            Created book
        """
        book = Book(
            **book_data.model_dump(),
            user_id=user_id
        )
        db.add(book)
        await db.commit()
        await db.refresh(book)
        logger.info(f"Created book: {book.id} by user {user_id}")
        return book

    @staticmethod
    async def get_book(db: AsyncSession, book_id: int, include_chapters: bool = False) -> Optional[Book]:
        """
        Get a book by ID

        Args:
            db: Database session
            book_id: Book ID
            include_chapters: Whether to include chapters and blocks

        Returns:
            Book or None
        """
        query = select(Book).where(Book.id == book_id)

        if include_chapters:
            query = query.options(
                selectinload(Book.chapters).selectinload(Chapter.blocks)
            )

        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_books(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50,
        user_id: Optional[int] = None,
        is_published: Optional[bool] = True,
        access_level: Optional[AccessLevel] = None
    ) -> List[Book]:
        """
        Get list of books with filters

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            user_id: Filter by user ID
            is_published: Filter by published status
            access_level: Filter by access level

        Returns:
            List of books
        """
        query = select(Book)

        if user_id is not None:
            query = query.where(Book.user_id == user_id)

        if is_published is not None:
            query = query.where(Book.is_published == is_published)

        if access_level is not None:
            query = query.where(Book.access_level == access_level)

        query = query.where(Book.is_blocked == False)
        query = query.order_by(Book.created_at.desc())
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def update_book(db: AsyncSession, book_id: int, book_data: BookUpdate) -> Optional[Book]:
        """
        Update a book

        Args:
            db: Database session
            book_id: Book ID
            book_data: Book update data

        Returns:
            Updated book or None
        """
        book = await BookService.get_book(db, book_id)
        if not book:
            return None

        update_data = book_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(book, field, value)

        await db.commit()
        await db.refresh(book)
        logger.info(f"Updated book: {book_id}")
        return book

    @staticmethod
    async def delete_book(db: AsyncSession, book_id: int) -> bool:
        """
        Delete a book

        Args:
            db: Database session
            book_id: Book ID

        Returns:
            True if deleted, False if not found
        """
        book = await BookService.get_book(db, book_id)
        if not book:
            return False

        await db.delete(book)
        await db.commit()
        logger.info(f"Deleted book: {book_id}")
        return True

    @staticmethod
    async def publish_book(db: AsyncSession, book_id: int) -> Optional[Book]:
        """
        Publish a book

        Args:
            db: Database session
            book_id: Book ID

        Returns:
            Published book or None
        """
        book = await BookService.get_book(db, book_id)
        if not book:
            return None

        book.is_published = True
        book.published_at = datetime.utcnow()
        await db.commit()
        await db.refresh(book)
        logger.info(f"Published book: {book_id}")
        return book

    @staticmethod
    async def generate_book(
        db: AsyncSession,
        user_id: int,
        generation_request: BookGenerationRequest
    ) -> Book:
        """
        Generate a book using AI

        Args:
            db: Database session
            user_id: User ID
            generation_request: Generation request data

        Returns:
            Generated book

        Raises:
            Exception: If generation fails
        """
        logger.info(f"Generating book for user {user_id}")

        # Generate book content using Gemini
        book_data = await gemini_service.generate_book(
            plot=generation_request.plot,
            language=generation_request.language,
            age_group=generation_request.age_group,
            pages=generation_request.pages,
            style=generation_request.style,
            system_prompt=generation_request.system_prompt
        )

        # Moderate content
        moderation = await gemini_service.moderate_content(
            f"{book_data.get('title')} {book_data.get('description')}"
        )

        if not moderation.get("is_safe", False):
            logger.warning(f"Generated content failed moderation: {moderation.get('issues')}")
            raise ValueError("Generated content contains inappropriate material")

        # Create book
        book = Book(
            user_id=user_id,
            title=book_data.get("title", "Untitled"),
            description=book_data.get("description", ""),
            language=generation_request.language,
            age_group=generation_request.age_group,
            access_level=AccessLevel.PUBLIC
        )
        db.add(book)
        await db.flush()  # Get book ID

        # Create chapters and blocks
        chapters_data = book_data.get("chapters", [])
        for chapter_data in chapters_data:
            chapter = Chapter(
                book_id=book.id,
                chapter_number=chapter_data.get("number", 1),
                title=chapter_data.get("title", f"Chapter {chapter_data.get('number', 1)}")
            )
            db.add(chapter)
            await db.flush()  # Get chapter ID

            # Add text block
            text_block = Block(
                chapter_id=chapter.id,
                block_type=BlockType.TEXT,
                content=chapter_data.get("content", ""),
                order_index=0
            )
            db.add(text_block)

            # Add illustration description block (for future image generation)
            if "illustration_prompt" in chapter_data:
                illustration_block = Block(
                    chapter_id=chapter.id,
                    block_type=BlockType.IMAGE,
                    content=chapter_data.get("illustration_prompt", ""),
                    order_index=1
                )
                db.add(illustration_block)

        await db.commit()
        await db.refresh(book)

        logger.info(f"Successfully generated book: {book.id}")
        return book

    @staticmethod
    async def increment_views(db: AsyncSession, book_id: int) -> None:
        """
        Increment book views count

        Args:
            db: Database session
            book_id: Book ID
        """
        book = await BookService.get_book(db, book_id)
        if book:
            book.views_count += 1
            await db.commit()
