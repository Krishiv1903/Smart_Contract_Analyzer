"""
ontology.py

Defines the ontology (schema) for the Legal Knowledge Graph.

The ontology specifies:
    - Node Types
    - Entity Types
    - Relation Types
    - Dependency Types

These enums ensure consistency across the entire project.
"""

from __future__ import annotations

from enum import Enum

# ==========================================================
# Node Types
# ==========================================================
class NodeType(str, Enum):
    """
    Types of nodes that can exist in the knowledge graph.
    """

    CLAUSE = "CLAUSE"
    PARTY = "PARTY"
    ACTION = "ACTION"
    OBLIGATION = "OBLIGATION"
    PERMISSION = "PERMISSION"
    PROHIBITION = "PROHIBITION"
    CONDITION = "CONDITION"
    EVENT = "EVENT"
    VALUE = "VALUE"
    DATE = "DATE"
    TIME = "TIME"
    DURATION = "DURATION"
    DEFINED_TERM = "DEFINED_TERM"
    DOCUMENT = "DOCUMENT"
    SECTION = "SECTION"
    RISK = "RISK"

# ==========================================================
# Entity Types
# ==========================================================
class EntityType(str, Enum):
    """
    Entity types extracted from clauses.
    """

    PARTY = "PARTY"
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    ACTION = "ACTION"
    VALUE = "VALUE"
    MONEY = "MONEY"
    DATE = "DATE"
    TIME = "TIME"
    DURATION = "DURATION"
    LOCATION = "LOCATION"
    WEBSITE = "WEBSITE"
    EMAIL = "EMAIL"
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"
    DEFINED_TERM = "DEFINED_TERM"
    LAW = "LAW"
    RISK = "RISK"

# ==========================================================
# Relation Types
# ==========================================================

class RelationType(str, Enum):
    """
    Relationships inside a clause.
    """
    HAS_ACTION = "HAS_ACTION"
    PERFORMS = "PERFORMS"
    RECEIVES = "RECEIVES"
    PAYS = "PAYS"
    OWNS = "OWNS"
    USES = "USES"
    DEFINES = "DEFINES"
    REFERENCES = "REFERENCES"
    HAS_VALUE = "HAS_VALUE"
    HAS_DATE = "HAS_DATE"
    HAS_TIME = "HAS_TIME"
    HAS_DURATION = "HAS_DURATION"
    HAS_CONDITION = "HAS_CONDITION"
    HAS_PERMISSION = "HAS_PERMISSION"
    HAS_PROHIBITION = "HAS_PROHIBITION"
    HAS_OBLIGATION = "HAS_OBLIGATION"
    HAS_RISK = "HAS_RISK"

# ==========================================================
# Dependency Types
# ==========================================================
class DependencyType(str, Enum):
    """
    Dependencies between clauses.
    """
    REFERENCES = "REFERENCES"
    DEPENDS_ON = "DEPENDS_ON"
    MODIFIES = "MODIFIES"
    OVERRIDES = "OVERRIDES"
    EXCEPTION_TO = "EXCEPTION_TO"
    DEFINES = "DEFINES"
    REQUIRES = "REQUIRES"
    EXTENDS = "EXTENDS"
    TERMINATES = "TERMINATES"
    ACTIVATES = "ACTIVATES"
    TRIGGERS = "TRIGGERS"
    CONFLICTS_WITH = "CONFLICTS_WITH"
    SUPPORTS = "SUPPORTS"


# ==========================================================
# Helper Functions
# ==========================================================

def node_types() -> list[str]:
    """Return all node types."""
    return [item.value for item in NodeType]


def entity_types() -> list[str]:
    """Return all entity types."""
    return [item.value for item in EntityType]


def relation_types() -> list[str]:
    """Return all relation types."""
    return [item.value for item in RelationType]


def dependency_types() -> list[str]:
    """Return all dependency types."""
    return [item.value for item in DependencyType]