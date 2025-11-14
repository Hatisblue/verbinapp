"""
Challenges API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime
from pydantic import BaseModel

from app.db.database import get_db
from app.models.user import User, UserRole
from app.models.other import Challenge, ChallengeParticipation
from app.middleware.auth_middleware import get_current_user, get_current_admin_user

router = APIRouter()

class ChallengeCreate(BaseModel):
    title: str
    description: str
    theme: str
    starts_at: datetime
    ends_at: datetime

class ChallengeResponse(BaseModel):
    id: int
    title: str
    description: str
    theme: str
    starts_at: str
    ends_at: str
    class Config:
        from_attributes = True

@router.get("", response_model=List[ChallengeResponse])
async def get_challenges(db: AsyncSession = Depends(get_db)):
    """Get all active challenges"""
    result = await db.execute(
        select(Challenge).where(Challenge.ends_at > datetime.utcnow()).order_by(Challenge.starts_at.desc())
    )
    challenges = result.scalars().all()
    return [ChallengeResponse(
        id=c.id, title=c.title, description=c.description or "", theme=c.theme or "",
        starts_at=str(c.starts_at), ends_at=str(c.ends_at)
    ) for c in challenges]

@router.post("", response_model=ChallengeResponse, status_code=status.HTTP_201_CREATED)
async def create_challenge(
    challenge_data: ChallengeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new challenge (admin only)"""
    challenge = Challenge(**challenge_data.model_dump(), admin_id=current_user.id)
    db.add(challenge)
    await db.commit()
    await db.refresh(challenge)
    return ChallengeResponse(
        id=challenge.id, title=challenge.title, description=challenge.description or "",
        theme=challenge.theme or "", starts_at=str(challenge.starts_at), ends_at=str(challenge.ends_at)
    )

@router.post("/{challenge_id}/join", status_code=status.HTTP_201_CREATED)
async def join_challenge(
    challenge_id: int, book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Join a challenge with a book"""
    participation = ChallengeParticipation(challenge_id=challenge_id, book_id=book_id)
    db.add(participation)
    await db.commit()
    return {"message": "Joined challenge successfully"}
