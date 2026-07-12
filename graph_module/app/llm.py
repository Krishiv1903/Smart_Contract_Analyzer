"""
llm.py
Unified LLM interface for the Legal Knowledge Graph.
Supports:
- Groq (Cloud)
- Ollama (Local)

Features
--------
✓ Automatic provider selection
✓ Automatic fallback (Groq -> Ollama)
✓ Prompt loading
✓ JSON response parsing
✓ Retry mechanism
✓ Logging
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import ollama
from groq import Groq

from app.config import config
from app.logger import get_logger
from app.exceptions import (
    LLMConnectionError,
    InvalidLLMResponseError,
)

logger = get_logger(__name__)

# ==========================================================
# Prompt Loader
# ==========================================================

class PromptLoader:
    """
    Loads prompt templates from prompts/ directory.
    """

    @staticmethod
    def load(prompt_name: str) -> str:
        path = config.PROMPT_DIR / prompt_name
        if not path.exists():
            raise FileNotFoundError(path)
        return path.read_text(
            encoding="utf-8"
        )


# ==========================================================
# Groq Client
# ==========================================================

class GroqClient:
    def __init__(self):
        self.client = Groq(
            api_key=config.GROQ_API_KEY
        )
        self.model = config.GROQ_MODEL

    def generate(self, prompt: str, temperature: float = 0.1,) -> str:
        logger.info("Sending request to Groq...")

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return response.choices[0].message.content or ""


# ==========================================================
# Ollama Client
# ==========================================================

class OllamaClient:

    def __init__(self):
        self.model = config.OLLAMA_MODEL

    def generate(self, prompt: str) -> str:
        logger.info("Sending request to Ollama...")
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return response["message"]["content"] or ""


# ==========================================================
# Manager
# ==========================================================

class LLMManager:
    """
    Main interface for the project.
    The rest of the project ONLY calls this class.
    """

    def __init__(self):
        self.provider = config.LLM_PROVIDER
        self.groq = GroqClient()
        self.ollama = OllamaClient()

    # ------------------------------------------------------

    def ask(self, prompt: str, retries: int = 2) -> str:
        for attempt in range(retries):
            try:
                if self.provider == "groq":
                    return self.groq.generate(prompt)
                return self.ollama.generate(prompt)
            except Exception as e:
                logger.warning("Attempt %d failed: %s", attempt + 1, e)
                time.sleep(1)

        logger.warning("Switching to Ollama fallback...")

        try:
            return self.ollama.generate(prompt)
        except Exception as e:
            raise LLMConnectionError(str(e))

    # ------------------------------------------------------

    def ask_json(self, prompt: str) -> dict:
        """
        Returns parsed JSON.
        """
        response = self.ask(prompt)
        try:
            return json.loads(response)
        except Exception:
            raise InvalidLLMResponseError("LLM returned invalid JSON.")

    # ------------------------------------------------------

    def ask_clause(self, clause: str, prompt_file: str) -> dict:
        """
        Uses one of the prompt templates.
        
        Parameters
        ----------
        clause

        prompt_file

        Returns
        -------
        dict
        """

        template = PromptLoader.load(prompt_file)
        prompt = template.replace("{{CLAUSE}}", clause)
        return self.ask_json(prompt)