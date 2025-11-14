"""
Chapters and Blocks API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import logging

from app.db.database import get_db
from app.models.user import User
from app.models.book import Book
from app.models.chapter import Chapter
from app.models.block import Block, BlockType
from app.middleware.auth_middleware import get_current_user
from pydantic import BaseModel

router = APIRouter()
logger = logging.getLogger(__name__)


# Schemas
class BlockCreate(BaseModel):
    block_type: str
    content: str
    order_index: int


class BlockUpdate(BaseModel):
    content: str = None
    order_index: int = None


class BlockResponse(BaseModel):
    id: int
    chapter_id: int
    block_type: str
    content: str
    order_index: int

    class Config:
        from_attributes = True


class ChapterCreate(BaseModel):
    chapter_number: int
    title: str = None


class ChapterResponse(BaseModel):
    id: int
    book_id: int
    chapter_number: int
    title: str = None
    blocks: List[BlockResponse] = []

    class Config:
        from_attributes = True


# Chapter endpoints
@router.get("/book/{book_id}/chapters", response_model=List[ChapterResponse])
async def get_book_chapters(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all chapters for a book"""
    # Check if book exists
    book_result = await db.execute(select(Book).where(Book.id == book_id))
    book = book_result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    # Get chapters with blocks
    from sqlalchemy.orm import selectinload
    query = select(Chapter).where(Chapter.book_id == book_id).options(
        selectinload(Chapter.blocks)
    ).order_by(Chapter.chapter_number)

    result = await db.execute(query)
    chapters = result.scalars().all()

    return [
        ChapterResponse(
            id=chapter.id,
            book_id=chapter.book_id,
            chapter_number=chapter.chapter_number,
            title=chapter.title,
            blocks=[
                BlockResponse(
                    id=block.id,
                    chapter_id=block.chapter_id,
                    block_type=block.block_type.value,
                    content=block.content or "",
                    order_index=block.order_index
                )
                for block in sorted(chapter.blocks, key=lambda b: b.order_index)
            ]
        )
        for chapter in chapters
    ]


@router.post("/book/{book_id}/chapters", response_model=ChapterResponse, status_code=status.HTTP_201_CREATED)
async def create_chapter(
    book_id: int,
    chapter_data: ChapterCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new chapter"""
    # Check if book exists and user owns it
    book_result = await db.execute(select(Book).where(Book.id == book_id))
    book = book_result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    if book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    # Create chapter
    chapter = Chapter(
        book_id=book_id,
        chapter_number=chapter_data.chapter_number,
        title=chapter_data.title
    )
    db.add(chapter)
    await db.commit()
    await db.refresh(chapter)

    return ChapterResponse(
        id=chapter.id,
        book_id=chapter.book_id,
        chapter_number=chapter.chapter_number,
        title=chapter.title,
        blocks=[]
    )


@router.delete("/chapters/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chapter(
    chapter_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a chapter"""
    chapter_result = await db.execute(select(Chapter).where(Chapter.id == chapter_id))
    chapter = chapter_result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")

    # Check if user owns the book
    book_result = await db.execute(select(Book).where(Book.id == chapter.book_id))
    book = book_result.scalar_one_or_none()
    if not book or book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    await db.delete(chapter)
    await db.commit()


# Block endpoints
@router.post("/chapters/{chapter_id}/blocks", response_model=BlockResponse, status_code=status.HTTP_201_CREATED)
async def create_block(
    chapter_id: int,
    block_data: BlockCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new block"""
    # Check if chapter exists
    chapter_result = await db.execute(select(Chapter).where(Chapter.id == chapter_id))
    chapter = chapter_result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")

    # Check if user owns the book
    book_result = await db.execute(select(Book).where(Book.id == chapter.book_id))
    book = book_result.scalar_one_or_none()
    if not book or book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    # Create block
    try:
        block_type_enum = BlockType(block_data.block_type)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid block type")

    block = Block(
        chapter_id=chapter_id,
        block_type=block_type_enum,
        content=block_data.content,
        order_index=block_data.order_index
    )
    db.add(block)
    await db.commit()
    await db.refresh(block)

    return BlockResponse(
        id=block.id,
        chapter_id=block.chapter_id,
        block_type=block.block_type.value,
        content=block.content or "",
        order_index=block.order_index
    )


@router.put("/blocks/{block_id}", response_model=BlockResponse)
async def update_block(
    block_id: int,
    block_data: BlockUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a block"""
    block_result = await db.execute(select(Block).where(Block.id == block_id))
    block = block_result.scalar_one_or_none()
    if not block:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Block not found")

    # Check if user owns the book
    chapter_result = await db.execute(select(Chapter).where(Chapter.id == block.chapter_id))
    chapter = chapter_result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")

    book_result = await db.execute(select(Book).where(Book.id == chapter.book_id))
    book = book_result.scalar_one_or_none()
    if not book or book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    # Update block
    if block_data.content is not None:
        block.content = block_data.content
    if block_data.order_index is not None:
        block.order_index = block_data.order_index

    await db.commit()
    await db.refresh(block)

    return BlockResponse(
        id=block.id,
        chapter_id=block.chapter_id,
        block_type=block.block_type.value,
        content=block.content or "",
        order_index=block.order_index
    )


@router.delete("/blocks/{block_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_block(
    block_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a block"""
    block_result = await db.execute(select(Block).where(Block.id == block_id))
    block = block_result.scalar_one_or_none()
    if not block:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Block not found")

    # Check if user owns the book
    chapter_result = await db.execute(select(Chapter).where(Chapter.id == block.chapter_id))
    chapter = chapter_result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")

    book_result = await db.execute(select(Book).where(Book.id == chapter.book_id))
    book = book_result.scalar_one_or_none()
    if not book or book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    await db.delete(block)
    await db.commit()


# Reorder blocks
class BlockReorderRequest(BaseModel):
    block_ids: List[int]  # List of block IDs in new order


@router.post("/chapters/{chapter_id}/blocks/reorder", status_code=status.HTTP_200_OK)
async def reorder_blocks(
    chapter_id: int,
    reorder_data: BlockReorderRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reorder blocks in a chapter (drag-and-drop support)"""
    # Check if chapter exists
    chapter_result = await db.execute(select(Chapter).where(Chapter.id == chapter_id))
    chapter = chapter_result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")

    # Check if user owns the book
    book_result = await db.execute(select(Book).where(Book.id == chapter.book_id))
    book = book_result.scalar_one_or_none()
    if not book or book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    # Update order_index for all blocks
    for new_index, block_id in enumerate(reorder_data.block_ids):
        block_result = await db.execute(select(Block).where(Block.id == block_id))
        block = block_result.scalar_one_or_none()
        if block and block.chapter_id == chapter_id:
            block.order_index = new_index

    await db.commit()

    return {"message": "Blocks reordered successfully"}
