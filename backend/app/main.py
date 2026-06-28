"""
Application entry point.
"""

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import get_logger, setup_logging


setup_logging()
logger = get_logger(__name__)

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application.
    """
    logger.info("Creating FastAPI application...")

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.app_debug,
    )

    app.include_router(
        api_router,
        prefix=settings.api_prefix,
    )
    
    logger.info("Application created successfully.")

    return app


app = create_app()
