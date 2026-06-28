"""
Database session configuration.

This module creates the SQLAlchemy Session factory used by the application.
"""

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.db.database import engine


SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)