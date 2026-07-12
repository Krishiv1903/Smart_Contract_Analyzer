"""
exceptions.py

Custom exceptions used throughout the LegalKnowledgeGraph project.

Using custom exceptions instead of generic ValueError or RuntimeError
makes debugging much easier and keeps error handling consistent.
"""


# ==========================================================
# Base Exception
# ==========================================================

class LegalKnowledgeGraphError(Exception):
    """
    Base exception for the entire project.
    """

    def __init__(self, message: str = "Legal Knowledge Graph Error"):
        super().__init__(message)


# ==========================================================
# Configuration
# ==========================================================

class ConfigurationError(LegalKnowledgeGraphError):
    """
    Raised when application configuration is invalid.
    """


class MissingEnvironmentVariableError(ConfigurationError):
    """
    Raised when a required environment variable is missing.
    """


# ==========================================================
# Input / Parser
# ==========================================================

class ParserError(LegalKnowledgeGraphError):
    """
    Base parser exception.
    """


class InvalidDocumentError(ParserError):
    """
    Raised when the input document is invalid.
    """


class UnsupportedFileFormatError(ParserError):
    """
    Raised when the input file format is unsupported.
    """


class InvalidJSONError(ParserError):
    """
    Raised when JSON parsing fails.
    """


class EmptyDocumentError(ParserError):
    """
    Raised when an empty document is supplied.
    """


# ==========================================================
# LLM
# ==========================================================

class LLMError(LegalKnowledgeGraphError):
    """
    Base LLM exception.
    """


class LLMConnectionError(LLMError):
    """
    Raised when the LLM cannot be reached.
    """


class InvalidLLMResponseError(LLMError):
    """
    Raised when the LLM response is malformed.
    """


class PromptError(LLMError):
    """
    Raised when a prompt cannot be loaded.
    """


# ==========================================================
# Extraction
# ==========================================================

class ExtractionError(LegalKnowledgeGraphError):
    """
    Base extraction exception.
    """


class EntityExtractionError(ExtractionError):
    """
    Raised when entity extraction fails.
    """


class RelationExtractionError(ExtractionError):
    """
    Raised when relation extraction fails.
    """


class DependencyExtractionError(ExtractionError):
    """
    Raised when dependency extraction fails.
    """


# ==========================================================
# Graph
# ==========================================================

class GraphError(LegalKnowledgeGraphError):
    """
    Base graph exception.
    """


class GraphConstructionError(GraphError):
    """
    Raised when graph creation fails.
    """


class InvalidNodeError(GraphError):
    """
    Raised when a graph node is invalid.
    """


class InvalidEdgeError(GraphError):
    """
    Raised when a graph edge is invalid.
    """


class DuplicateNodeError(GraphError):
    """
    Raised when duplicate nodes are detected.
    """


class DuplicateEdgeError(GraphError):
    """
    Raised when duplicate edges are detected.
    """


class GraphValidationError(GraphError):
    """
    Raised when the generated graph is invalid.
    """


# ==========================================================
# Export
# ==========================================================

class ExportError(LegalKnowledgeGraphError):
    """
    Raised when graph export fails.
    """


class VisualizationError(LegalKnowledgeGraphError):
    """
    Raised when graph visualization fails.
    """


# ==========================================================
# Cache
# ==========================================================

class CacheError(LegalKnowledgeGraphError):
    """
    Raised when cache operations fail.
    """


# ==========================================================
# Utility
# ==========================================================

class FileOperationError(LegalKnowledgeGraphError):
    """
    Raised when reading or writing files fails.
    """