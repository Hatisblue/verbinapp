"""
Comments API endpoints
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_comments():
    """Get comments (placeholder)"""
    return []
