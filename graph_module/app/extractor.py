"""
extractor.py

Hybrid information extraction module.

Pipeline

Clause
   │
   ▼
Regex Extraction
   │
   ▼
spaCy Extraction
   │
   ▼
LLM Extraction
   │
   ▼
Merge Results
   │
   ▼
Entities
Relations
Dependencies

This is the heart of the Legal Knowledge Graph.
"""

from __future__ import annotations

import re
import spacy

from app.logger import get_logger
from app.models import (
    Clause,
    Entity,
    Relation,
    Dependency,
)
from app.ontology import (
    EntityType,
    RelationType,
    DependencyType,
)
from app.llm import LLMManager

logger = get_logger(__name__)

class Extractor:
    """
    Hybrid extractor.

    Uses
    1. Regex
    2. spaCy
    3. LLM

    and merges everything together.
    """

    def __init__(self):
        logger.info("Loading spaCy model...")
        self.nlp = spacy.load("en_core_web_sm")
        self.llm = LLMManager()

    # ==========================================================
    # Public API
    # ==========================================================
    def extract(self, clause: Clause) -> tuple[list[Entity], list[Relation], list[Dependency]]:
        logger.info("Extracting Clause %s", clause.id)
        entities = []
        relations = []
        dependencies = []

        entities.extend(self.regex_entities(clause))
        entities.extend(self.spacy_entities(clause))
        
        llm_output = self.llm.ask_clause(clause.text, "entity_prompt.md")

        entities.extend(self.parse_llm_entities(clause, llm_output))
        entities = self.remove_duplicates(entities)

        return (
            entities,
            relations,
            dependencies,
        )

    # ==========================================================
    # Regex
    # ==========================================================
    def regex_entities(self, clause: Clause) -> list[Entity]:
        entities = []
        patterns = {
            EntityType.DATE: r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
            EntityType.EMAIL: r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
            EntityType.WEBSITE: r"https?://[^\s]+",
            EntityType.MONEY: r"\$\d+(?:,\d+)*(?:\.\d+)?",
            EntityType.DURATION: r"\b\d+\s*(day|days|month|months|year|years|hour|hours)\b",
        }

        for entity_type, pattern in patterns.items():
            matches = re.findall(
                pattern,
                clause.text,
                flags=re.IGNORECASE,
            )

            for value in matches:
                entities.append(
                    Entity(
                        id=f"REGEX_{len(entities)+1}",
                        clause_id=clause.id,
                        type=entity_type.value,
                        value=str(value),
                        confidence=0.95,
                    )
                )
        return entities

    # ==========================================================
    # spaCy
    # ==========================================================
    def spacy_entities(self, clause: Clause) -> list[Entity]:
        doc = self.nlp(clause.text)
        entities = []
        for ent in doc.ents:
            entities.append(
                Entity(
                    id=f"SPACY_{len(entities)+1}",
                    clause_id=clause.id,
                    type=ent.label_,
                    value=ent.text,
                    confidence=0.90,
                )
            )
        return entities

    # ==========================================================
    # LLM
    # ==========================================================
    def parse_llm_entities(self, clause: Clause, response: dict) -> list[Entity]:
        entities = []
        for item in response.get("entities", []):
            entities.append(
                Entity(
                    id=item["id"],
                    clause_id=clause.id,
                    type=item["type"],
                    value=item["value"],
                    confidence=item.get("confidence", 1.0),
                )
            )
        return entities

    # ==========================================================
    # Merge
    # ==========================================================
    def remove_duplicates(self, entities: list[Entity]) -> list[Entity]:
        seen = set()
        unique = []
        for entity in entities:
            key = (entity.type.lower(), entity.value.lower())
            if key not in seen:
                seen.add(key)
                unique.append(entity)
        return unique

    # ==========================================================
    # Future
    # ==========================================================
    def extract_relations(self, clause: Clause) -> list[Relation]:
        """
        Implemented later.
        """
        return []

    def extract_dependencies(self, clause: Clause) -> list[Dependency]:
        """
        Implemented later.
        """
        return []