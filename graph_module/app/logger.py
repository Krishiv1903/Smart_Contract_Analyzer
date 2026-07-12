"""
logger.py

Centralized logging configuration for the LegalKnowledgeGraph project.
Features
--------
- Console logging
- File logging
- Colored console output (using Rich if available)
- Singleton logger
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import config

try:
    from rich.logging import RichHandler
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

class Logger:
    """
    Singleton logger for the entire application.
    """

    _initialized = False
    @classmethod
    def setup(cls) -> None:
        """
        Configure application logging.
        """

        if cls._initialized:
            return

        log_file = Path(config.LOG_FILE)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        root_logger = logging.getLogger()
        root_logger.setLevel(config.LOG_LEVEL)

        # Remove duplicate handlers
        root_logger.handlers.clear()

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # ----------------------------------------------------
        # Console Handler
        # ----------------------------------------------------
        if RICH_AVAILABLE:
            console_handler = RichHandler(
                rich_tracebacks=True,
                markup=True,
                show_path=False,
            )
        else:
            console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        # ----------------------------------------------------
        # File Handler
        # ----------------------------------------------------
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=5 * 1024 * 1024,   # 5 MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        cls._initialized = True

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger.

    Parameters
    ----------
    name : str
        Usually __name__

    Returns
    -------
    logging.Logger
    """

    Logger.setup()
    return logging.getLogger(name)