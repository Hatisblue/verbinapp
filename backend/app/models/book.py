"""
Book model
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base


class AccessLevel(str, enum.Enum):
    """Book access level enum"""
    PUBLIC = "public"
    REGISTERED = "registered"
    SUBSCRIBERS = "subscribers"
    PREMIUM_TIER = "premium_tier"
    PRIVATE = "private"


class Book(Base):
    """Book model"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    cover_url = Column(String(500), nullable=True)
    language = Column(String(10), default="ru", nullable=False)
    age_group = Column(String(50), nullable=True)  # '7-9', '10-12'
    access_level = Column(SQLEnum(AccessLevel), default=AccessLevel.PUBLIC, nullable=False)
    premium_tier_rating = Column(Integer, nullable=True)  # Minimum rating for premium tier access
    views_count = Column(Integer, default=0, nullable=False)
    likes_count = Column(Integer, default=0, nullable=False)
    comments_count = Column(Integer, default=0, nullable=False)
    average_reading_time = Column(Integer, nullable=True)  # In minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)
    block_reason = Column(Text, nullable=True)

    # Relationships
    author = relationship("User", back_populates="books")
    chapters = relationship("Chapter", back_populates="book", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="book", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="book", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="book", cascade="all, delete-orphan")
    book_categories = relationship("BookCategory", back_populates="book", cascade="all, delete-orphan")
    book_tags = relationship("BookTag", back_populates="book", cascade="all, delete-orphan")
    challenge_participations = relationship("ChallengeParticipation", back_populates="book", cascade="all, delete-orphan")
    content_reports = relationship("ContentReport", back_populates="book", cascade="all, delete-orphan")
    book_versions = relationship("BookVersion", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author_id={self.user_id})>"
