"""
Like model
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Like(Base):
    """Like model"""
    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint('user_id', 'book_id', name='unique_user_book_like'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="likes")
    book = relationship("Book", back_populates="likes")

    def __repr__(self):
        return f"<Like(id={self.id}, user_id={self.user_id}, book_id={self.book_id})>"
