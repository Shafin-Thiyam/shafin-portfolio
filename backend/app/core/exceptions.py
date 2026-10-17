"""
Global exception handlers.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        """
        Handle FastAPI HTTP exceptions.
        """

        logger.warning(
            "HTTP %s - %s",
            exc.status_code,
            exc.detail,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """
        Handle request validation errors.
        """
        validation_errors = exc.errors()
        logger.warning(
            "Request validation failed.",
            len(validation_errors)
            )
        errors = [
            {
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"],
            }
            for error in validation_errors
        ]

        return JSONResponse(
            status_code=422,
            content={
                "detail": errors,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Handle unexpected exceptions.
        """

        logger.exception("Unhandled exception occurred.")

        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal Server Error",
            },
        )