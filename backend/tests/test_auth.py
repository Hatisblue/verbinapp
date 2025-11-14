"""
Tests for authentication endpoints
"""
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register():
    """Test user registration"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "TestPassword123"
            }
        )
        assert response.status_code in [201, 409]  # Created or Conflict (already exists)

@pytest.mark.asyncio
async def test_login():
    """Test user login"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First register
        await client.post(
            "/api/auth/register",
            json={
                "email": "test2@example.com",
                "username": "testuser2",
                "password": "TestPassword123"
            }
        )

        # Then login
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "test2@example.com",
                "password": "TestPassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
