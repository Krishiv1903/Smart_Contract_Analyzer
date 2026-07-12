"""
    dependency.py

    Clause Dependency Detection
    This module discovers relationships BETWEEN clauses.

    Example
    Clause 4:
    "The user must comply with Clause 2."
        ↓
    Dependency
    Clause 4 --------REFERENCES-------> Clause 2

    This module combines
        1. Rule-based detection
        2. Similarity detection
        3. LLM reasoning
    to build the dependency graph.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher

from app.logger import get_logger
from app.llm import LLMManager
from app.models import Clause, Dependency
from app.ontology import DependencyType

logger = get_logger(__name__)

class DependencyDetector:
    """
    Detects dependencies between clauses.
    """
    def __init__(self):
        self.llm = LLMManager()

    # =====================================================
    # Public API
    # =====================================================
    def detect(self, clauses: list[Clause]) -> list[Dependency]:
        """
        Detect dependencies between every pair of clauses.
        """
        logger.info("Detecting clause dependencies...")

        dependencies = []
        n = len(clauses)
        for i in range(n):
            for j in range(i + 1, n):
                clause_a = clauses[i]
                clause_b = clauses[j]
                dep = self.rule_based_detection(clause_a, clause_b)
                if dep is not None:
                    dependencies.append(dep)
                    continue
                dep = self.similarity_detection(clause_a, clause_b)
                if dep is not None:
                    dependencies.append(dep)
        logger.info("Detected %d dependencies.", len(dependencies))
        return dependencies

    # =====================================================
    # Rule Based
    # =====================================================
    def rule_based_detection(self, clause_a: Clause, clause_b: Clause) -> Dependency | None:
        text = clause_a.text.lower()
        # ---------------------------------------------
        if clause_b.id.lower() in text:
            return Dependency(
                id=f"DEP_{clause_a.id}_{clause_b.id}",
                source_clause=clause_a.id,
                target_clause=clause_b.id,
                relation=DependencyType.REFERENCES.value,
                confidence=1.0,
                reason="Explicit clause reference.",
            )

        # ---------------------------------------------
        keywords = {
            "except": DependencyType.EXCEPTION_TO,
            "unless": DependencyType.EXCEPTION_TO,
            "subject to": DependencyType.DEPENDS_ON,
            "according to": DependencyType.REFERENCES,
            "defined in": DependencyType.DEFINES,
            "pursuant to": DependencyType.REFERENCES,
            "under": DependencyType.DEPENDS_ON,
        }
        for keyword, relation in keywords.items():
            if keyword in text:
                return Dependency(
                    id=f"DEP_{clause_a.id}_{clause_b.id}",
                    source_clause=clause_a.id,
                    target_clause=clause_b.id,
                    relation=relation.value,
                    confidence=0.90,
                    reason=f"Keyword '{keyword}' detected.",
                )
        return None

    # =====================================================
    # Similarity
    # =====================================================
    def similarity_detection(self, clause_a: Clause, clause_b: Clause, threshold: float = 0.65) -> Dependency | None:
        score = SequenceMatcher(None, clause_a.text.lower(), clause_b.text.lower()).ratio()
        if score >= threshold:
            return Dependency(
                id=f"SIM_{clause_a.id}_{clause_b.id}",
                source_clause=clause_a.id,
                target_clause=clause_b.id,
                relation=DependencyType.SUPPORTS.value,
                confidence=score,
                reason="High textual similarity.",
            )
        return None

    # =====================================================
    # LLM Detection
    # =====================================================
    def llm_detection(self, clause_a: Clause, clause_b: Clause) -> Dependency | None:
        """
        Uses Groq/Ollama to detect semantic dependencies.
        This is more expensive than rule-based methods and should be used only if required.
        """

        prompt = f"""
            You are a legal expert.

            Determine whether these two clauses have a dependency.

            Return ONLY JSON.

            {{
                "dependent": true/false,
                "relation":"REFERENCES",
                "reason":"..."
            }}

            Clause A
            {clause_a.text}

            Clause B
            {clause_b.text}
        """
        response = self.llm.ask_json(prompt)
        if not response.get("dependent", False):
            return None

        return Dependency(
            id=f"LLM_{clause_a.id}_{clause_b.id}",
            source_clause=clause_a.id,
            target_clause=clause_b.id,
            relation=response["relation"],
            confidence=0.95,
            reason=response["reason"],
        )

    # =====================================================
    # Utility
    # =====================================================
    @staticmethod
    def dependency_matrix(clauses: list[Clause], dependencies: list[Dependency]) -> list[list[int]]:
        """
        Creates an adjacency matrix.
        """

        ids = [c.id for c in clauses]
        index = {
            cid: i
            for i, cid in enumerate(ids)
        }
        matrix = [
            [0 for _ in ids]
            for _ in ids
        ]
        for dep in dependencies:
            i = index[dep.source_clause]
            j = index[dep.target_clause]
            matrix[i][j] = 1
        return matrix