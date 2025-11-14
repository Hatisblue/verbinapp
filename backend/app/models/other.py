"""
Other models: Notification, Favorite, Challenge, Achievement, etc.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base


class NotificationType(str, enum.Enum):
    """Notification type enum"""
    COMMENT = "comment"
    LIKE = "like"
    CHALLENGE_RESULT = "challenge_result"
    SUBSCRIPTION = "subscription"
    RECOMMENDATION = "recommendation"


class Notification(Base):
    """Notification model"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    notification_type = Column(SQLEnum(NotificationType), nullable=False)
    related_book_id = Column(Integer, ForeignKey("books.id", ondelete="SET NULL"), nullable=True)
    related_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="notifications", foreign_keys=[user_id])

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.notification_type}, read={self.is_read})>"


class Favorite(Base):
    """Favorite model"""
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="favorites")
    book = relationship("Book", back_populates="favorites")

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, book_id={self.book_id})>"


class Challenge(Base):
    """Challenge model"""
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    theme = Column(String(255), nullable=True)
    starts_at = Column(DateTime(timezone=True), nullable=False)
    ends_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    participations = relationship("ChallengeParticipation", back_populates="challenge")

    def __repr__(self):
        return f"<Challenge(id={self.id}, title={self.title})>"


class ChallengeParticipation(Base):
    """Challenge participation model"""
    __tablename__ = "challenge_participations"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    winner = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    challenge = relationship("Challenge", back_populates="participations")
    book = relationship("Book", back_populates="challenge_participations")

    def __repr__(self):
        return f"<ChallengeParticipation(id={self.id}, challenge_id={self.challenge_id}, book_id={self.book_id}, winner={self.winner})>"


class Achievement(Base):
    """Achievement model"""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement")

    def __repr__(self):
        return f"<Achievement(id={self.id}, name={self.name})>"


class UserAchievement(Base):
    """User achievement model"""
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="user_achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")

    def __repr__(self):
        return f"<UserAchievement(id={self.id}, user_id={self.user_id}, achievement_id={self.achievement_id})>"


class GenerationType(str, enum.Enum):
    """Generation type enum"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"


class GenerationStatus(str, enum.Enum):
    """Generation status enum"""
    SUCCESS = "success"
    FAILED = "failed"


class GenerationLog(Base):
    """Generation log model"""
    __tablename__ = "generation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="SET NULL"), nullable=True)
    generation_type = Column(SQLEnum(GenerationType), nullable=False)
    status = Column(SQLEnum(GenerationStatus), nullable=False)
    error_message = Column(Text, nullable=True)
    generation_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="generation_logs")

    def __repr__(self):
        return f"<GenerationLog(id={self.id}, user_id={self.user_id}, type={self.generation_type}, status={self.status})>"


class BookVersion(Base):
    """Book version model for version history"""
    __tablename__ = "book_versions"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, nullable=False)
    content = Column(JSON, nullable=True)  # Full snapshot of the book
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    change_description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    book = relationship("Book", back_populates="book_versions")

    def __repr__(self):
        return f"<BookVersion(id={self.id}, book_id={self.book_id}, version={self.version_number})>"


class BonusReason(str, enum.Enum):
    """Bonus generation reason enum"""
    HIGH_RATING = "high_rating"
    CHALLENGE_WINNER = "challenge_winner"
    REFERRAL = "referral"


class BonusGeneration(Base):
    """Bonus generation model"""
    __tablename__ = "bonus_generations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    bonus_count = Column(Integer, nullable=False)
    reason = Column(SQLEnum(BonusReason), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<BonusGeneration(id={self.id}, user_id={self.user_id}, count={self.bonus_count}, reason={self.reason})>"


class ReportReason(str, enum.Enum):
    """Content report reason enum"""
    INAPPROPRIATE = "inappropriate"
    OFFENSIVE = "offensive"
    SPAM = "spam"
    OTHER = "other"


class ReportStatus(str, enum.Enum):
    """Content report status enum"""
    PENDING = "pending"
    REVIEWED = "reviewed"
    DISMISSED = "dismissed"
    ACTIONED = "actioned"


class ContentReport(Base):
    """Content report model"""
    __tablename__ = "content_reports"

    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    report_reason = Column(SQLEnum(ReportReason), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(ReportStatus), default=ReportStatus.PENDING, nullable=False)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    action_taken = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    book = relationship("Book", back_populates="content_reports")

    def __repr__(self):
        return f"<ContentReport(id={self.id}, book_id={self.book_id}, reason={self.report_reason}, status={self.status})>"


class AdminAction(str, enum.Enum):
    """Admin action enum"""
    USER_BLOCKED = "user_blocked"
    USER_UNBLOCKED = "user_unblocked"
    BOOK_DELETED = "book_deleted"
    BOOK_RESTORED = "book_restored"
    COMMENT_DELETED = "comment_deleted"
    CHALLENGE_CREATED = "challenge_created"


class AdminLog(Base):
    """Admin log model"""
    __tablename__ = "admin_logs"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(SQLEnum(AdminAction), nullable=False)
    target_id = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<AdminLog(id={self.id}, admin_id={self.admin_id}, action={self.action})>"
