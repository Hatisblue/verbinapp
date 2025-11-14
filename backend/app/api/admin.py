"""
Admin API endpoints
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def admin_dashboard():
    """Admin dashboard (placeholder)"""
    return {"status": "ok"}
