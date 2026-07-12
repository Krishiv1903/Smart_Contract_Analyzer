"""
utils.py

Common utility functions used across the Legal Knowledge Graph project.

Contains:
- UUID generation
- File handling
- JSON utilities
- Hashing
- Retry decorator
- Timing decorator
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from functools import wraps
from pathlib import Path
from typing import Any, Callable

from app.logger import get_logger

logger = get_logger(__name__)


# ==========================================================
# ID Generation
# ==========================================================

def generate_id(prefix: str) -> str:
    """
    Generate unique IDs.

    Example
    -------
    ENTITY_8af2c9d4
    """

    return f"{prefix.upper()}_{uuid.uuid4().hex[:8]}"


# ==========================================================
# File Utilities
# ==========================================================

def ensure_directory(path: str | Path) -> Path:
    """
    Create directory if it doesn't exist.
    """

    path = Path(path)

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path


def read_text(path: str | Path) -> str:

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(
    path: str | Path,
    text: str,
) -> None:

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


# ==========================================================
# JSON Utilities
# ==========================================================

def load_json(
    path: str | Path,
) -> dict:

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(
    data: dict,
    path: str | Path,
) -> None:

    with open(path, "w", encoding="utf-8") as f:

        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False,

        )


# ==========================================================
# Hash Utilities
# ==========================================================

def hash_text(
    text: str,
) -> str:
    """
    SHA256 hash of text.
    """

    return hashlib.sha256(

        text.encode("utf-8")

    ).hexdigest()


def hash_file(
    path: str | Path,
) -> str:

    sha = hashlib.sha256()

    with open(path, "rb") as f:

        while True:

            chunk = f.read(8192)

            if not chunk:
                break

            sha.update(chunk)

    return sha.hexdigest()


# ==========================================================
# Retry Decorator
# ==========================================================

def retry(
    attempts: int = 3,
    delay: int = 2,
):
    """
    Retry decorator.

    Example
    -------

    @retry()

    def foo():
        ...
    """

    def decorator(func):

        @wraps(func)

        def wrapper(*args, **kwargs):

            last_exception: Exception = RuntimeError(
                f"Failed to execute {func.__name__} after {attempts} attempts"
            )

            for i in range(attempts):

                try:

                    return func(
                        *args,
                        **kwargs,
                    )

                except Exception as e:

                    last_exception = e

                    logger.warning(

                        "%s failed (%d/%d)",

                        func.__name__,

                        i + 1,

                        attempts,

                    )

                    time.sleep(delay)

            raise last_exception

        return wrapper

    return decorator


# ==========================================================
# Timer Decorator
# ==========================================================

def timer(func):
    """
    Measure execution time.
    """

    @wraps(func)

    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        result = func(
            *args,
            **kwargs,
        )

        end = time.perf_counter()

        logger.info(

            "%s completed in %.3f seconds",

            func.__name__,

            end - start,

        )

        return result

    return wrapper


# ==========================================================
# Pretty Printing
# ==========================================================

def separator(
    title: str | None = None,
) -> None:

    logger.info("=" * 70)

    if title:

        logger.info(title.upper())

        logger.info("=" * 70)


# ==========================================================
# Statistics
# ==========================================================

def percentage(
    part: int,
    total: int,
) -> float:

    if total == 0:
        return 0.0

    return round(

        (part / total) * 100,

        2,

    )


# ==========================================================
# List Helpers
# ==========================================================

def unique(
    items: list[Any],
) -> list[Any]:
    """
    Remove duplicates while preserving order.
    """

    seen = set()

    output = []

    for item in items:

        if item not in seen:

            output.append(item)

            seen.add(item)

    return output


# ==========================================================
# Text Helpers
# ==========================================================

def normalize_text(
    text: str,
) -> str:
    """
    Normalize whitespace.
    """

    return " ".join(

        text.split()

    ).strip()


def truncate(
    text: str,
    length: int = 100,
) -> str:

    if len(text) <= length:
        return text

    return text[:length] + "..." 