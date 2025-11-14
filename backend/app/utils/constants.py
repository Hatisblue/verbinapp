"""
Application constants
"""
import os
from typing import List

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "False") == "True"

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# CORS
CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Rate limiting
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))

# Subscription plans
SUBSCRIPTION_LIMITS = {
    "free": {
        "generation_limit": 5,
        "storage_mb": 10,
        "price": 0,
    },
    "basic": {
        "generation_limit": 20,
        "storage_mb": 100,
        "price_monthly": 200,
        "price_yearly": 999,
    },
    "premium": {
        "generation_limit": -1,  # Unlimited
        "storage_mb": 1000,
        "price_monthly": 500,
        "price_yearly": 2999,
    }
}

# Bonus generations
BONUS_GENERATION_THRESHOLDS = {
    "1000_likes": 5,  # +5 generations for 1000+ likes
    "5000_likes": 10,  # +10 generations for 5000+ likes
}

# Pagination
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100

# File upload
MAX_FILE_SIZE_MB = 10
ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".gif"]
ALLOWED_AUDIO_EXTENSIONS = [".mp3", ".wav", ".ogg"]
ALLOWED_VIDEO_EXTENSIONS = [".mp4", ".webm", ".avi"]

# Generation
DEFAULT_GENERATION_LANGUAGE = "ru"
DEFAULT_AGE_GROUP = "7-12"
DEFAULT_PAGES_PER_GENERATION = 10
MAX_PAGES_PER_GENERATION = 20
