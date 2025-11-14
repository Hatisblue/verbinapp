"""
AI BookCreator - Main Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging

from app.middleware.error_handler import error_handler_middleware
from app.middleware.auth_middleware import AuthMiddleware
from app.db.database import engine, Base
from app.utils.logger import setup_logging
from app.api import auth, books, users, comments, payments, admin, notifications, recommendations, challenges

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting AI BookCreator application...")

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Application started successfully")
    yield

    logger.info("Shutting down AI BookCreator application...")
    await engine.dispose()


# Create FastAPI app
app = FastAPI(
    title="AI BookCreator API",
    description="API for AI-powered book creation platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# CORS middleware
from app.utils.constants import CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Custom middlewares
app.middleware("http")(error_handler_middleware)
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(books.router, prefix="/api/books", tags=["Books"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(comments.router, prefix="/api/comments", tags=["Comments"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(challenges.router, prefix="/api/challenges", tags=["Challenges"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI BookCreator API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
