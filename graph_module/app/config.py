"""
config.py

Application configuration loader.
Loads environment variables from .env and exposes them through a singleton configuration object.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# --------------------------------------------------------
# Load .env
# --------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"
load_dotenv(ENV_PATH)

# --------------------------------------------------------
# Configuration
# --------------------------------------------------------
@dataclass(slots=True)
class Config:
    """
    Global application configuration.
    """

    # =====================================================
    # Project
    # =====================================================
    PROJECT_NAME: str = "LegalKnowledgeGraph"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # =====================================================
    # LLM
    # =====================================================
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq").lower()
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    # =====================================================
    # spaCy
    # =====================================================
    SPACY_MODEL: str = os.getenv("SPACY_MODEL", "en_core_web_sm")

    # =====================================================
    # Paths
    # =====================================================
    ROOT_DIR: Path = ROOT_DIR
    INPUT_DIR: Path = ROOT_DIR / "input"
    OUTPUT_DIR: Path = ROOT_DIR / "output"
    JSON_OUTPUT_DIR: Path = OUTPUT_DIR / "json"
    HTML_OUTPUT_DIR: Path = OUTPUT_DIR / "html"
    GRAPH_OUTPUT_DIR: Path = OUTPUT_DIR / "graphs"
    LOG_DIR: Path = ROOT_DIR / "logs"
    PROMPT_DIR: Path = ROOT_DIR / "prompts"
    CACHE_DIR: Path = ROOT_DIR / "cache"

    # =====================================================
    # Graph
    # =====================================================
    GRAPH_LAYOUT: str = "spring"
    SAVE_GRAPHML: bool = True
    SAVE_JSON: bool = True
    SAVE_HTML: bool = True

    # =====================================================
    # Logging
    # =====================================================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Path = LOG_DIR / "application.log"

    # =====================================================
    # Cache
    # =====================================================
    ENABLE_CACHE: bool = True
    CACHE_EXPIRY_DAYS: int = 30

    # =====================================================
    # Utility
    # =====================================================
    def create_directories(self) -> None:
        """
        Create all required directories.
        """
        directories = [
            self.INPUT_DIR,
            self.OUTPUT_DIR,
            self.JSON_OUTPUT_DIR,
            self.HTML_OUTPUT_DIR,
            self.GRAPH_OUTPUT_DIR,
            self.LOG_DIR,
            self.PROMPT_DIR,
            self.CACHE_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------
# Singleton Configuration
# --------------------------------------------------------
config = Config()
config.create_directories()