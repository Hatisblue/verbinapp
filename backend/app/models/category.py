"""
Category and Tag models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Category(Base):
    """Category model"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    book_categories = relationship("BookCategory", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, slug={self.slug})>"


class Tag(Base):
    """Tag model"""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    book_tags = relationship("BookTag", back_populates="tag")

    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name}, slug={self.slug})>"


class BookCategory(Base):
    """Book-Category association table"""
    __tablename__ = "book_categories"

    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)

    # Relationships
    book = relationship("Book", back_populates="book_categories")
    category = relationship("Category", back_populates="book_categories")

    def __repr__(self):
        return f"<BookCategory(book_id={self.book_id}, category_id={self.category_id})>"


class BookTag(Base):
    """Book-Tag association table"""
    __tablename__ = "book_tags"

    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

    # Relationships
    book = relationship("Book", back_populates="book_tags")
    tag = relationship("Tag", back_populates="book_tags")

    def __repr__(self):
        return f"<BookTag(book_id={self.book_id}, tag_id={self.tag_id})>"
