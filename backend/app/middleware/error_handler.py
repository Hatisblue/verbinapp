"""
Error handling middleware
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


async def error_handler_middleware(request: Request, call_next):
    """
    Global error handling middleware

    Catches and formats all exceptions
    """
    try:
        response = await call_next(request)
        return response

    except RequestValidationError as e:
        logger.warning(f"Validation error: {e}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation Error",
                "detail": e.errors()
            }
        )

    except IntegrityError as e:
        logger.error(f"Database integrity error: {e}")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "Database Integrity Error",
                "detail": "A database constraint was violated. The resource may already exist."
            }
        )

    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Database Error",
                "detail": "An error occurred while accessing the database."
            }
        )

    except Exception as e:
        logger.exception(f"Unhandled exception: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "detail": str(e) if logger.level == logging.DEBUG else "An unexpected error occurred."
            }
        )
