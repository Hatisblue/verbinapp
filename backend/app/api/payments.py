"""
Payments API endpoints
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_payments():
    """Get payments (placeholder)"""
    return []
