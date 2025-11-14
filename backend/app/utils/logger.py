"""
Logging configuration
"""
import logging
import sys
from typing import Optional

def setup_logging(level: Optional[str] = None):
    """
    Setup application logging

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    if level is None:
        level = "DEBUG" if __import__("os").getenv("DEBUG", "False") == "True" else "INFO"

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log") if __import__("os").getenv("ENVIRONMENT") != "development" else logging.NullHandler(),
        ]
    )

    # Set third-party loggers to WARNING
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {level}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(name)
