"""
Authentication middleware
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Authentication middleware

    Handles JWT token validation and user context
    """

    # Public endpoints that don't require authentication
    PUBLIC_ENDPOINTS = [
        "/",
        "/health",
        "/api/docs",
        "/api/redoc",
        "/api/openapi.json",
        "/api/auth/register",
        "/api/auth/login",
        "/api/auth/refresh",
        "/api/books",  # Public books can be viewed without auth
    ]

    async def dispatch(self, request: Request, call_next):
        """
        Process request and validate authentication if required
        """
        # Skip authentication for public endpoints
        if any(request.url.path.startswith(endpoint) for endpoint in self.PUBLIC_ENDPOINTS):
            return await call_next(request)

        # Check for Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            logger.debug(f"No authorization header for: {request.url.path}")
            # Allow request to proceed; endpoint-level dependencies will handle auth
            return await call_next(request)

        # Validate token format
        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid authorization header format. Expected 'Bearer <token>'"}
            )

        # Extract token (validation will be done at endpoint level)
        token = auth_header.replace("Bearer ", "")
        request.state.token = token

        return await call_next(request)


# Dependency for getting current user from token
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.utils.constants import SECRET_KEY, ALGORITHM
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current user from JWT token

    Args:
        credentials: HTTP authorization credentials
        db: Database session

    Returns:
        Current user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        # Decode JWT token
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_blocked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is blocked",
        )

    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current user and verify admin role

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if admin

    Raises:
        HTTPException: If user is not an admin
    """
    from app.models.user import UserRole

    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin or Moderator role required."
        )

    return current_user


async def get_optional_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User | None:
    """
    Get current user if authenticated, None otherwise

    Useful for endpoints that work for both authenticated and anonymous users

    Args:
        request: HTTP request
        db: Database session

    Returns:
        Current user or None
    """
    token = getattr(request.state, "token", None)
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            return None

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if user and not user.is_blocked:
            return user

    except JWTError:
        return None

    return None
