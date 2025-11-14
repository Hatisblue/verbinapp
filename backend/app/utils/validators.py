"""
Validation utilities
"""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Validate email format

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength

    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"

    return True, None


def validate_username(username: str) -> tuple[bool, Optional[str]]:
    """
    Validate username format

    Requirements:
    - 3-50 characters
    - Alphanumeric, underscores, and hyphens only
    - No spaces

    Args:
        username: Username to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"

    if len(username) > 50:
        return False, "Username must be at most 50 characters long"

    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"

    return True, None


def sanitize_html(text: str) -> str:
    """
    Sanitize HTML content to prevent XSS

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text
    """
    import bleach

    allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'a']
    allowed_attributes = {'a': ['href', 'title']}

    return bleach.clean(text, tags=allowed_tags, attributes=allowed_attributes, strip=True)


def validate_file_extension(filename: str, allowed_extensions: list[str]) -> bool:
    """
    Validate file extension

    Args:
        filename: Filename to validate
        allowed_extensions: List of allowed extensions (e.g., ['.jpg', '.png'])

    Returns:
        True if valid, False otherwise
    """
    import os
    _, ext = os.path.splitext(filename.lower())
    return ext in allowed_extensions
