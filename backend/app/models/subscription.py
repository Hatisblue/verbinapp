"""
Subscription model
"""
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base


class SubscriptionPlan(str, enum.Enum):
    """Subscription plan enum"""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"


class Subscription(Base):
    """Subscription model"""
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    plan = Column(SQLEnum(SubscriptionPlan), default=SubscriptionPlan.FREE, nullable=False)
    generation_limit = Column(Integer, default=5, nullable=False)  # Generations per month
    generations_used = Column(Integer, default=0, nullable=False)
    starts_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="subscriptions")
    payments = relationship("Payment", back_populates="subscription")

    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, plan={self.plan}, active={self.is_active})>"
