"""
Notifications API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.database import get_db
from app.models.user import User
from app.models.other import Notification
from app.middleware.auth_middleware import get_current_user

router = APIRouter()

@router.get("")
async def get_notifications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user notifications"""
    result = await db.execute(
        select(Notification).where(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc()).limit(50)
    )
    notifications = result.scalars().all()
    return [{"id": n.id, "message": n.message, "is_read": n.is_read} for n in notifications]

@router.put("/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark notification as read"""
    result = await db.execute(select(Notification).where(Notification.id == notification_id))
    notification = result.scalar_one_or_none()
    if notification and notification.user_id == current_user.id:
        notification.is_read = True
        await db.commit()
    return {"message": "Marked as read"}
