"""
Database dependencies.

This module provides reusable FastAPI dependencies for database access.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session for the current request.

    Yields:
        SQLAlchemy database session.

    Ensures:
        The session is always closed after the request completes.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()