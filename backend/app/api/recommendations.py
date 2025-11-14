"""
Recommendations API endpoints
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_recommendations():
    """Get recommendations (placeholder)"""
    return []
