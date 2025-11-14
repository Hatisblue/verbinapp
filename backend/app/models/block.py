"""
Block model (Notion-like blocks)
"""
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base


class BlockType(str, enum.Enum):
    """Block type enum"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DIALOG = "dialog"
    TABLE = "table"
    CODE = "code"


class Block(Base):
    """Block model - Notion-like content blocks"""
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    block_type = Column(SQLEnum(BlockType), nullable=False)
    content = Column(Text, nullable=True)  # JSON for complex types
    order_index = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    chapter = relationship("Chapter", back_populates="blocks")

    def __repr__(self):
        return f"<Block(id={self.id}, chapter_id={self.chapter_id}, type={self.block_type}, order={self.order_index})>"
