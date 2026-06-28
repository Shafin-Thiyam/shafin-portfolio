
"""
Centralized logging configuration for the application.

This module is responsible for:
- configuring the logging system
- providing module-specific loggers
"""

import logging

from app.core.config import settings


DEFAULT_LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)


def setup_logging() -> None:
    """
    Configure application logging.
    """

    logging.basicConfig(
        level=settings.log_level.value,
        format=DEFAULT_LOG_FORMAT,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a module-specific logger.

    Args:
        name: Module name.

    Returns:
        Configured logger.
    """

    return logging.getLogger(name)