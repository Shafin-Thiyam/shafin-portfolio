"""
Application entry point.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.exceptions import register_exception_handlers
from app.middleware import register_middlewares
from app.core.config import settings
from app.core.logging import get_logger, setup_logging


setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manage application startup and shutdown events.
    """

    logger.info("Application startup.")

    yield

    logger.info("Application shutdown.")


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
        lifespan=lifespan,
        )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:5174",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    register_exception_handlers(app)
    
    register_middlewares(app)


    app.include_router(
        api_router,
        prefix=settings.api_prefix,
    )
    
    logger.info("Application created successfully.")

    return app


app = create_app()
