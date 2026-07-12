"""
models.py

Core data models used throughout the Legal Knowledge Graph project.

Pipeline

Document
    ├── Clause
    │      ├── Entity
    │      ├── Relation
    │      └── Dependency
    │
    └── KnowledgeGraph
            ├── Node
            └── Edge
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, ConfigDict

# ==========================================================
# Clause
# ==========================================================
class Clause(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    section: str = "General"
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    @property
    def word_count(self) -> int:
        return len(self.text.split())

# ==========================================================
# Document
# ==========================================================
class Document(BaseModel):
    model_config = ConfigDict(extra="ignore")
    document_id: str
    title: str
    source: str = ""
    version: str = "1.0"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)
    clauses: list[Clause] = Field(default_factory=list)
    @property
    def clause_count(self) -> int:
        return len(self.clauses)

# ==========================================================
# Entity
# ==========================================================
class Entity(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    clause_id: str
    type: str
    value: str
    confidence: float = 1.0
    metadata: dict[str, Any] = Field(default_factory=dict)

# ==========================================================
# Relation
# ==========================================================
class Relation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    clause_id: str
    source_entity: str
    target_entity: str
    relation: str
    confidence: float = 1.0
    metadata: dict[str, Any] = Field(default_factory=dict)

# ==========================================================
# Dependency
# ==========================================================
class Dependency(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    source_clause: str
    target_clause: str
    relation: str
    confidence: float = 1.0
    reason: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)

# ==========================================================
# Graph Node
# ==========================================================
class Node(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    label: str
    type: str
    source_id: str
    clause_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

# ==========================================================
# Graph Edge
# ==========================================================

class Edge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    source: str
    target: str
    relation: str
    confidence: float = 1.0
    metadata: dict[str, Any] = Field(default_factory=dict)

# ==========================================================
# Knowledge Graph
# ==========================================================
class KnowledgeGraph(BaseModel):
    model_config = ConfigDict(extra="ignore")
    document_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    nodes: list[Node] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    @property
    def node_count(self) -> int:
        return len(self.nodes)
    @property
    def edge_count(self) -> int:
        return len(self.edges)
    def add_node(self, node: Node) -> None:
        if node.id not in {n.id for n in self.nodes}:
            self.nodes.append(node)
    def add_edge(self, edge: Edge) -> None:
        if edge.id not in {e.id for e in self.edges}:
            self.edges.append(edge)

# ==========================================================
# LLM Response
# ==========================================================
class LLMResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    provider: str
    model: str
    clause_id: str
    raw_response: str
    entities: list[Entity] = Field(default_factory=list)
    relations: list[Relation] = Field(default_factory=list)
    dependencies: list[Dependency] = Field(default_factory=list)
    processing_time: float = 0.0