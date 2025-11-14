"""
Chapter model
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Chapter(Base):
    """Chapter model"""
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    book = relationship("Book", back_populates="chapters")
    blocks = relationship("Block", back_populates="chapter", cascade="all, delete-orphan", order_by="Block.order_index")

    def __repr__(self):
        return f"<Chapter(id={self.id}, book_id={self.book_id}, number={self.chapter_number}, title={self.title})>"
