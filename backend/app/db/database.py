"""
Database engine configuration.

This module creates the SQLAlchemy Engine used by the application.
"""

from sqlalchemy import Engine
from sqlalchemy import create_engine

from app.core.config import settings


engine: Engine = create_engine(
    settings.database_url,
    echo=settings.app_debug,
    pool_pre_ping=True,
)