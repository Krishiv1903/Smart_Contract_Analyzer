"""
graph_builder.py

Builds the Legal Knowledge Graph from extracted data.

Pipeline

Document
    │
    ▼
Entities
Relations
Dependencies
    │
    ▼
Knowledge Graph
    │
    ▼
NetworkX Graph

This module is responsible for creating the graph that will
later be visualized using PyVis.
"""

from __future__ import annotations

import networkx as nx

from app.logger import get_logger
from app.models import (
    Clause,
    Dependency,
    Edge,
    Entity,
    KnowledgeGraph,
    Node,
    Relation,
)
from app.ontology import NodeType

logger = get_logger(__name__)

class GraphBuilder:
    """
    Builds the complete Legal Knowledge Graph.
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    # =====================================================
    # Public API
    # =====================================================
    def build(
        self,
        document_id: str,
        clauses: list[Clause],
        entities: list[Entity],
        relations: list[Relation],
        dependencies: list[Dependency],
    ) -> KnowledgeGraph:

        logger.info("Building Knowledge Graph...")
        kg = KnowledgeGraph(document_id=document_id)

        # -----------------------------------------
        # Clause Nodes
        # -----------------------------------------
        for clause in clauses:
            node = Node(
                id=clause.id,
                label=clause.section,
                type=NodeType.CLAUSE.value,
                source_id=clause.id,
                clause_id=clause.id,
                metadata={
                    "text": clause.text
                }
            )
            kg.add_node(node)
            self.graph.add_node(node.id, label=node.label, type=node.type, title=clause.text)

        # -----------------------------------------
        # Entity Nodes
        # -----------------------------------------
        for entity in entities:
            node = Node(
                id=entity.id,
                label=entity.value,
                type=entity.type,
                source_id=entity.id,
                clause_id=entity.clause_id,
            )
            kg.add_node(node)
            self.graph.add_node(node.id, label=node.label, type=node.type)
            edge = Edge(
                id=f"EDGE_{entity.clause_id}_{entity.id}",
                source=entity.clause_id,
                target=entity.id,
                relation="HAS_ENTITY",
            )
            kg.add_edge(edge)
            self.graph.add_edge(edge.source, edge.target, relation=edge.relation)

        # -----------------------------------------
        # Relations
        # -----------------------------------------
        for relation in relations:
            edge = Edge(
                id=relation.id,
                source=relation.source_entity,
                target=relation.target_entity,
                relation=relation.relation,
                confidence=relation.confidence,
            )
            kg.add_edge(edge)
            self.graph.add_edge(edge.source, edge.target, relation=edge.relation)

        # -----------------------------------------
        # Clause Dependencies
        # -----------------------------------------
        for dependency in dependencies:
            edge = Edge(
                id=dependency.id,
                source=dependency.source_clause,
                target=dependency.target_clause,
                relation=dependency.relation,
                confidence=dependency.confidence,
            )
            kg.add_edge(edge)
            self.graph.add_edge(edge.source, edge.target, relation=edge.relation)
        logger.info("Graph Created | Nodes=%d Edges=%d", kg.node_count, kg.edge_count)
        return kg

    # =====================================================
    # Utilities
    # =====================================================
    def get_networkx_graph(self) -> nx.DiGraph:
        """
        Returns the underlying NetworkX graph.
        """
        return self.graph

    def statistics(self) -> dict:
        """
        Returns graph statistics.
        """
        G = self.graph
        return {
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "density": nx.density(G),
            "connected_components": nx.number_weakly_connected_components(G),
            "average_degree": sum(dict(G.degree()).values()) / max(G.number_of_nodes(), 1),
        }

    def articulation_points(self):
        G = self.graph.to_undirected()
        return list(nx.articulation_points(G))

    def bridges(self):
        G = self.graph.to_undirected()
        return list(nx.bridges(G))

    def shortest_path(self, source: str, target: str):
        try:
            return nx.shortest_path(self.graph, source, target)
        except:
            return None

    def find_orphan_nodes(self):
        G = self.graph
        return [
            n
            for n in G.nodes()
            if G.degree(n) == 0
        ]

    def centrality(self):
        return nx.degree_centrality(self.graph)

    def pagerank(self):
        return nx.pagerank(self.graph)

    def k_core(self):
        try:
            return nx.k_core(self.graph.to_undirected())
        except:
            return None