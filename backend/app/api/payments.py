"""
Payments and Subscriptions API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime, timedelta
from pydantic import BaseModel
import logging

from app.db.database import get_db
from app.models.user import User
from app.models.subscription import Subscription, SubscriptionPlan
from app.models.payment import Payment, PaymentStatus, PaymentMethod
from app.middleware.auth_middleware import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)


# Schemas
class SubscriptionPlanInfo(BaseModel):
    name: str
    generation_limit: int
    storage_mb: int
    price_monthly: int = None
    price_yearly: int = None


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan: str
    generation_limit: int
    generations_used: int
    is_active: bool
    expires_at: str = None

    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    amount: float
    plan: str
    billing_period: str = "monthly"  # monthly or yearly


class PaymentResponse(BaseModel):
    id: int
    amount: float
    status: str
    created_at: str

    class Config:
        from_attributes = True


# Get available plans
@router.get("/plans", response_model=List[SubscriptionPlanInfo])
async def get_subscription_plans():
    """Get available subscription plans"""
    from app.utils.constants import SUBSCRIPTION_LIMITS

    plans = [
        SubscriptionPlanInfo(
            name="free",
            generation_limit=SUBSCRIPTION_LIMITS["free"]["generation_limit"],
            storage_mb=SUBSCRIPTION_LIMITS["free"]["storage_mb"],
            price_monthly=0,
            price_yearly=0
        ),
        SubscriptionPlanInfo(
            name="basic",
            generation_limit=SUBSCRIPTION_LIMITS["basic"]["generation_limit"],
            storage_mb=SUBSCRIPTION_LIMITS["basic"]["storage_mb"],
            price_monthly=SUBSCRIPTION_LIMITS["basic"]["price_monthly"],
            price_yearly=SUBSCRIPTION_LIMITS["basic"]["price_yearly"]
        )
    ]
    return plans


# Get current subscription
@router.get("/subscription", response_model=SubscriptionResponse)
async def get_current_subscription(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user subscription"""
    result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == current_user.id,
            Subscription.is_active == True
        ).order_by(Subscription.created_at.desc())
    )
    subscription = result.scalar_one_or_none()

    if not subscription:
        # Create free subscription
        subscription = Subscription(
            user_id=current_user.id,
            plan=SubscriptionPlan.FREE,
            generation_limit=5,
            generations_used=0,
            is_active=True
        )
        db.add(subscription)
        await db.commit()
        await db.refresh(subscription)

    return SubscriptionResponse(
        id=subscription.id,
        user_id=subscription.user_id,
        plan=subscription.plan.value,
        generation_limit=subscription.generation_limit,
        generations_used=subscription.generations_used,
        is_active=subscription.is_active,
        expires_at=str(subscription.expires_at) if subscription.expires_at else None
    )


# Create payment
@router.post("/pay", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new payment (integrates with YooKassa)"""
    # Create payment record
    payment = Payment(
        user_id=current_user.id,
        amount=payment_data.amount,
        status=PaymentStatus.PENDING,
        payment_method=PaymentMethod.YANDEX_KASSA,
        transaction_id=f"txn_{current_user.id}_{int(datetime.utcnow().timestamp())}"
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)

    # TODO: Integrate with YooKassa API
    # For MVP, auto-approve payment
    payment.status = PaymentStatus.COMPLETED
    await db.commit()

    # Update subscription
    result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == current_user.id,
            Subscription.is_active == True
        ).order_by(Subscription.created_at.desc())
    )
    subscription = result.scalar_one_or_none()

    if subscription:
        subscription.is_active = False

    # Create new subscription
    from app.utils.constants import SUBSCRIPTION_LIMITS
    plan_info = SUBSCRIPTION_LIMITS.get(payment_data.plan, SUBSCRIPTION_LIMITS["free"])

    expires_days = 30 if payment_data.billing_period == "monthly" else 365
    new_subscription = Subscription(
        user_id=current_user.id,
        plan=SubscriptionPlan(payment_data.plan),
        generation_limit=plan_info["generation_limit"],
        generations_used=0,
        is_active=True,
        expires_at=datetime.utcnow() + timedelta(days=expires_days)
    )
    db.add(new_subscription)
    payment.subscription_id = new_subscription.id

    await db.commit()

    return PaymentResponse(
        id=payment.id,
        amount=float(payment.amount),
        status=payment.status.value,
        created_at=str(payment.created_at)
    )


# Cancel subscription
@router.post("/subscription/cancel", status_code=status.HTTP_200_OK)
async def cancel_subscription(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel current subscription"""
    result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == current_user.id,
            Subscription.is_active == True
        )
    )
    subscription = result.scalar_one_or_none()

    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active subscription")

    subscription.is_active = False

    # Create free subscription
    free_subscription = Subscription(
        user_id=current_user.id,
        plan=SubscriptionPlan.FREE,
        generation_limit=5,
        generations_used=0,
        is_active=True
    )
    db.add(free_subscription)
    await db.commit()

    return {"message": "Subscription cancelled successfully"}


# Get payment history
@router.get("/history", response_model=List[PaymentResponse])
async def get_payment_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get payment history"""
    result = await db.execute(
        select(Payment).where(Payment.user_id == current_user.id).order_by(Payment.created_at.desc())
    )
    payments = result.scalars().all()

    return [
        PaymentResponse(
            id=payment.id,
            amount=float(payment.amount),
            status=payment.status.value,
            created_at=str(payment.created_at)
        )
        for payment in payments
    ]
