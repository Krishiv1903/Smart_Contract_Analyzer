"""
exporter.py

Exports the Legal Knowledge Graph into multiple formats.

Supported Formats
-----------------
1. JSON
2. GraphML
3. NetworkX Pickle (optional)

Output Directory
----------------
output/
    ├── json/
    ├── graphml/
    └── graphs/
"""

from __future__ import annotations

from pathlib import Path
import json
import networkx as nx

from app.config import config
from app.logger import get_logger
from app.models import KnowledgeGraph

logger = get_logger(__name__)

class GraphExporter:
    """
    Handles exporting the knowledge graph.
    """

    def __init__(self):
        self.json_dir = config.JSON_OUTPUT_DIR
        self.graphml_dir = config.OUTPUT_DIR / "graphml"
        self.graphml_dir.mkdir(parents=True, exist_ok=True)

    # =====================================================
    # JSON Export
    # =====================================================
    def export_json(self, graph: KnowledgeGraph, filename: str = "knowledge_graph.json") -> Path:
        """
        Export KnowledgeGraph as JSON.
        """

        output_path = self.json_dir / filename
        graph_dict = graph.model_dump(mode="json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(graph_dict, f, indent=4, ensure_ascii=False)
        logger.info("JSON exported -> %s", output_path)
        return output_path

    # =====================================================
    # GraphML Export
    # =====================================================
    def export_graphml(self, nx_graph: nx.DiGraph, filename: str = "knowledge_graph.graphml") -> Path:
        """
        Export NetworkX graph as GraphML.
        """

        output_path = self.graphml_dir / filename
        nx.write_graphml(nx_graph, output_path)
        logger.info("GraphML exported -> %s", output_path)
        return output_path

    # =====================================================
    # GEXF Export
    # =====================================================
    def export_gexf(self, nx_graph: nx.DiGraph, filename: str = "knowledge_graph.gexf") -> Path:
        """
        Export graph to GEXF.
        Can be opened in Gephi.
        """

        output_path = self.graphml_dir / filename
        nx.write_gexf(

            nx_graph,

            output_path,

        )

        logger.info(
            "GEXF exported -> %s",
            output_path,
        )

        return output_path

    # =====================================================
    # Adjacency List
    # =====================================================

    def export_adjacency_list(
        self,
        nx_graph: nx.DiGraph,
        filename: str = "adjacency_list.txt",
    ) -> Path:
        """
        Export adjacency list.
        """

        output_path = self.graphml_dir / filename

        nx.write_adjlist(

            nx_graph,

            output_path,

        )

        logger.info(
            "Adjacency list exported."
        )

        return output_path

    # =====================================================
    # Complete Export
    # =====================================================

    def export_all(
        self,
        knowledge_graph: KnowledgeGraph,
        nx_graph: nx.DiGraph,
    ) -> dict:
        """
        Export every supported format.
        """

        logger.info(
            "Exporting Knowledge Graph..."
        )

        outputs = {}

        outputs["json"] = self.export_json(
            knowledge_graph
        )

        outputs["graphml"] = self.export_graphml(
            nx_graph
        )

        outputs["gexf"] = self.export_gexf(
            nx_graph
        )

        outputs["adjacency"] = self.export_adjacency_list(
            nx_graph
        )

        logger.info(
            "All exports completed."
        )

        return outputs

    # =====================================================
    # Utility
    # =====================================================

    @staticmethod
    def print_export_summary(
        outputs: dict,
    ) -> None:

        logger.info("")

        logger.info("=" * 60)

        logger.info("EXPORT SUMMARY")

        logger.info("=" * 60)

        for name, path in outputs.items():

            logger.info(
                "%-12s : %s",
                name,
                path,
            )

        logger.info("=" * 60)