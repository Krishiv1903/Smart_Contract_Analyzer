"""
parser.py

Loads legal documents and converts them into internal Document objects.

Supported input formats
-----------------------
- JSON (current)
- TXT (future)
- PDF (future)
- DOCX (future)

Expected JSON Format
--------------------

{
    "document_id": "DOC001",
    "title": "Google Terms of Service",
    "source": "https://...",
    "version": "2025",

    "clauses": [
        {
            "id": "C1",
            "section": "Introduction",
            "text": "Welcome to Google..."
        },
        {
            "id": "C2",
            "section": "Privacy",
            "text": "We collect..."
        }
    ]
}
"""

from __future__ import annotations

import json
from pathlib import Path

from app.logger import get_logger
from app.models import Clause, Document
from app.exceptions import (
    InvalidDocumentError,
    InvalidJSONError,
    UnsupportedFileFormatError,
)

logger = get_logger(__name__)

class Parser:
    """
    Responsible for loading input documents.
    """

    SUPPORTED_EXTENSIONS = { ".json" }

    def __init__(self) -> None:
        logger.info("Parser initialized.")

    # =====================================================
    # Public API
    # =====================================================

    def load(self, file_path: str | Path) -> Document:
        """
        Load any supported file.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(path)

        extension = path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise UnsupportedFileFormatError(
                f"{extension} is not supported."
            )

        if extension == ".json":
            return self._load_json(path)

        raise UnsupportedFileFormatError(extension)

    # =====================================================
    # JSON
    # =====================================================

    def _load_json(self, path: Path) -> Document:
        """
        Load JSON document.
        """

        logger.info(f"Loading {path.name}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise InvalidJSONError(str(e))

        return self.parse(data)

    # =====================================================
    # Parse Dictionary
    # =====================================================

    def parse(self, data: dict) -> Document:
        """
        Convert dictionary into Document.
        """

        self._validate(data)
        clauses = []
        for item in data["clauses"]:
            clause = Clause(
                id=item["id"],
                section=item.get("section", "General"),
                text=item["text"],
                metadata=item.get("metadata", {}),
            )
            clauses.append(clause)

        document = Document(
            document_id=data["document_id"],
            title=data["title"],
            source=data.get("source", ""),
            version=data.get("version", "1.0"),
            metadata=data.get("metadata", {}),
            clauses=clauses,
        )
        logger.info("Loaded '%s' (%d clauses)", document.title, document.clause_count)
        return document

    # =====================================================
    # Validation
    # =====================================================

    def _validate(self, data: dict) -> None:
        """
        Validate input dictionary.
        """
        required = [
            "document_id",
            "title",
            "clauses",
        ]

        for field in required:
            if field not in data:
                raise InvalidDocumentError(
                    f"Missing field '{field}'"
                )

        if not isinstance(data["clauses"], list):
            raise InvalidDocumentError("'clauses' must be a list.")
        if len(data["clauses"]) == 0:
            raise InvalidDocumentError("No clauses found.")

        ids = set()

        for clause in data["clauses"]:
            if "id" not in clause:
                raise InvalidDocumentError("Clause missing id.")
            if "text" not in clause:
                raise InvalidDocumentError("Clause missing text.")
            if clause["id"] in ids:
                raise InvalidDocumentError(f"Duplicate clause id {clause['id']}")
            ids.add(clause["id"])

    # =====================================================
    # Utility
    # =====================================================

    @staticmethod
    def document_summary(document: Document,) -> dict:
        """
        Returns summary of loaded document.
        """

        return {
            "title": document.title,
            "document_id": document.document_id,
            "clauses": document.clause_count,
            "source": document.source,
            "version": document.version,
        }