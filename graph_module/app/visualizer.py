"""
visualizer.py

Creates interactive and static visualizations for the
Legal Knowledge Graph.

Outputs
-------
1. Interactive HTML (PyVis)
2. Static PNG (Matplotlib)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network

from app.config import config
from app.logger import get_logger

logger = get_logger(__name__)

class GraphVisualizer:
    """
    Visualizes the Legal Knowledge Graph.
    Supports
    - Interactive HTML
    - Static PNG
    """

    def __init__(self):
        self.color_map = {
            "CLAUSE": "#4A90E2",
            "PARTY": "#27AE60",
            "ACTION": "#E67E22",
            "OBLIGATION": "#C0392B",
            "PERMISSION": "#8E44AD",
            "PROHIBITION": "#D35400",
            "VALUE": "#16A085",
            "DATE": "#F39C12",
            "TIME": "#9B59B6",
            "DURATION": "#1ABC9C",
            "DEFINED_TERM": "#2980B9",
            "DOCUMENT": "#2C3E50",
            "SECTION": "#7F8C8D",
            "RISK": "#E74C3C",
        }

    # ==========================================================
    # Interactive Graph
    # ==========================================================
    def save_html(self, graph: nx.DiGraph, filename: str = "knowledge_graph.html") -> Path:
        logger.info("Generating HTML visualization...")
        net = Network(
            height="900px",
            width="100%",
            directed=True,
            bgcolor="#ffffff",
        )
        net.barnes_hut()

        # ----------------------------------------
        # Nodes
        # ----------------------------------------
        for node, attrs in graph.nodes(data=True):
            node_type = attrs.get("type", "UNKNOWN")
            color = self.color_map.get(node_type, "#95A5A6")
            label = attrs.get("label", node)
            title = attrs.get("title", label)
            net.add_node(
                node,
                label=label,
                title=title,
                color=color,
                shape="dot",
                size=20,
            )

        # ----------------------------------------
        # Edges
        # ----------------------------------------
        for source, target, attrs in graph.edges(data=True):
            relation = attrs.get("relation", "")
            net.add_edge(source, target, label=relation, arrows="to")
        output_path = (config.HTML_OUTPUT_DIR / filename)
        net.save_graph(str(output_path))
        logger.info("Saved HTML visualization -> %s", output_path)
        return output_path

    # ==========================================================
    # Static Image
    # ==========================================================
    def save_png(self, graph: nx.DiGraph, filename: str = "knowledge_graph.png") -> Path:
        logger.info("Generating PNG graph...")
        plt.figure(figsize=(18, 14))
        pos = nx.spring_layout(graph, k=1.2, iterations=150, seed=42)
        colors = []
        labels = {}
        for node, attrs in graph.nodes(data=True):
            node_type = attrs.get("type", "UNKNOWN")
            colors.append(self.color_map.get(node_type, "#BDC3C7"))
            labels[node] = attrs.get("label", node)

        nx.draw_networkx_nodes(graph, pos, node_color=colors, node_size=1600)
        nx.draw_networkx_labels(graph, pos, labels, font_size=8)
        nx.draw_networkx_edges(graph, pos, arrows=True, arrowstyle="-|>", arrowsize=18)

        edge_labels = {}
        for u, v, attrs in graph.edges(data=True):
            edge_labels[(u, v)] = attrs.get("relation", "")

        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=7)
        plt.axis("off")

        output_path = (config.GRAPH_OUTPUT_DIR / filename)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        logger.info("Saved PNG graph -> %s", output_path)
        return output_path

    # ==========================================================
    # Statistics
    # ==========================================================
    def print_summary(self, graph: nx.DiGraph) -> None:
        logger.info("=" * 60)
        logger.info("GRAPH SUMMARY")
        logger.info("=" * 60)
        logger.info("Nodes : %d", graph.number_of_nodes())
        logger.info("Edges : %d", graph.number_of_edges())
        logger.info("Density : %.4f", nx.density(graph))
        logger.info(
            "Connected Components : %d",
            nx.number_weakly_connected_components(graph)
        )
        logger.info("=" * 60)

    # ==========================================================
    # Complete Visualization
    # ==========================================================
    def visualize(self, graph: nx.DiGraph) -> dict:
        html = self.save_html(graph)
        png = self.save_png(graph)
        self.print_summary(graph)
        return {
            "html": html,
            "png": png,
        }