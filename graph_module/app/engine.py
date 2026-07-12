"""
engine.py

Main orchestration engine for the Legal Knowledge Graph.

Pipeline

Input JSON
    │
    ▼
Parser
    │
    ▼
Entity Extraction
    │
    ▼
Dependency Detection
    │
    ▼
Graph Builder
    │
    ▼
Visualization
    │
    ▼
Export

This is the only class the application should interact with.
"""

from __future__ import annotations
from pathlib import Path

from app.logger import get_logger
from app.parser import Parser
from app.extractor import Extractor
from app.dependency import DependencyDetector
from app.graph_builder import GraphBuilder
from app.visualizer import GraphVisualizer
from app.exporter import GraphExporter
from app.utils import timer, separator

logger = get_logger(__name__)

class LegalKnowledgeGraphEngine:
    """
    Main Engine.
    Executes the complete Legal Knowledge Graph pipeline.
    """

    def __init__(self):
        logger.info("=" * 70)
        logger.info("Initializing Legal Knowledge Graph Engine")
        logger.info("=" * 70)
        self.parser = Parser()
        self.extractor = Extractor()
        self.dependency_detector = DependencyDetector()
        self.graph_builder = GraphBuilder()
        self.visualizer = GraphVisualizer()
        self.exporter = GraphExporter()
        logger.info("Engine initialized successfully.")

    # ==========================================================
    # Public API
    # ==========================================================

    @timer
    def process_document(self, file_path: str | Path):
        """
        Complete document processing pipeline.
        """
        separator("STEP 1 : Loading Document")
        document = self.parser.load(file_path)
        
        separator("STEP 2 : Entity Extraction")
        entities = []
        relations = []
        for clause in document.clauses:
            clause_entities, clause_relations, _ = self.extractor.extract(clause)
            entities.extend(clause_entities)
            relations.extend(clause_relations)
        logger.info("Extracted %d entities",len(entities),)
        logger.info("Extracted %d relations", len(relations))

        separator("STEP 3 : Dependency Detection")
        dependencies = self.dependency_detector.detect(document.clauses)
        logger.info("Detected %d dependencies", len(dependencies))

        separator("STEP 4 : Graph Construction")
        knowledge_graph = self.graph_builder.build(
            document.document_id,
            document.clauses,
            entities,
            relations,
            dependencies,
        )
        nx_graph = self.graph_builder.get_networkx_graph()
        stats = self.graph_builder.statistics()
        logger.info("Graph Statistics")
        for key, value in stats.items():
            logger.info("%s : %s", key, value)

        separator("STEP 5 : Visualization")
        visualization_files = self.visualizer.visualize(nx_graph)
        
        separator("STEP 6 : Export")
        export_files = self.exporter.export_all(knowledge_graph, nx_graph)
        self.exporter.print_export_summary(export_files)

        separator("PROCESS COMPLETED")
        logger.info("Knowledge Graph generated successfully.")

        return {
            "document": document,
            "knowledge_graph": knowledge_graph,
            "networkx_graph": nx_graph,
            "entities": entities,
            "relations": relations,
            "dependencies": dependencies,
            "statistics": stats,
            "visualization": visualization_files,
            "exports": export_files,
        }

    # ==========================================================
    # Convenience Methods
    # ==========================================================

    def visualize_only(self, nx_graph):
        return self.visualizer.visualize(nx_graph)

    def export_only(self, knowledge_graph, nx_graph,):
        return self.exporter.export_all(knowledge_graph, nx_graph)

    def graph_statistics(self):
        return self.graph_builder.statistics()

    def shortest_path(self, source, target,):
        return self.graph_builder.shortest_path(source, target)

    def articulation_points(self):
        return self.graph_builder.articulation_points()

    def bridges(self):
        return self.graph_builder.bridges()

    def centrality(self):
        return self.graph_builder.centrality()

    def pagerank(self):
        return self.graph_builder.pagerank()