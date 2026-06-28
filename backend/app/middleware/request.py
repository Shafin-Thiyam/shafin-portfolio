"""
Application request/response middleware.

This module is responsible for:

- Logging incoming HTTP requests
- Logging outgoing HTTP responses
- Measuring request processing time
"""

from time import perf_counter
from collections.abc import Callable, Awaitable
from fastapi import FastAPI, Request
from starlette.responses import Response

from app.core.logging import get_logger

logger = get_logger(__name__)


def register_middlewares(app: FastAPI) -> None:
    """
    Register application middleware.
    """

    @app.middleware("http")
    async def request_logging_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """
        Log request and response information.

        Args:
            request: Incoming HTTP request.
            call_next: Next middleware or route handler.

        Returns:
            HTTP response.
        """

        start_time = perf_counter()
        
        
        client_ip = request.client.host if request.client else "unknown"

        logger.info(
            "Incoming Request | %s | %s | %s",
            request.method,
            request.url.path,
            client_ip,
        )

        response = await call_next(request)

        duration_ms = (perf_counter() - start_time) * 1000

        logger.info(
            "Completed Request | %s | %s | %s | %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response