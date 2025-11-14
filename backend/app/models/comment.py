"""
Comment model
"""
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base


class CommentStatus(str, enum.Enum):
    """Comment status enum"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Comment(Base):
    """Comment model"""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)
    content = Column(Text, nullable=False)
    status = Column(SQLEnum(CommentStatus), default=CommentStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="comments")
    book = relationship("Book", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")

    def __repr__(self):
        return f"<Comment(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, status={self.status})>"
