"""
main.py

Entry point for the Legal Knowledge Graph project.

Pipeline

Input JSON
    ↓
Parser
    ↓
Entity Extraction
    ↓
Relation Extraction
    ↓
Dependency Detection
    ↓
Knowledge Graph
    ↓
Visualization
    ↓
Export
"""

from pathlib import Path
import traceback

from app.engine import LegalKnowledgeGraphEngine
from app.logger import get_logger

logger = get_logger(__name__)


def print_banner() -> None:
    """Print project banner."""

    print("\n")
    print("=" * 80)
    print("          LEGAL KNOWLEDGE GRAPH")
    print("      Terms & Conditions Graph Generator")
    print("=" * 80)
    print()


def main():
    print_banner()
    # --------------------------------------------------
    # Input document
    # --------------------------------------------------

    input_file = Path("input/sample_document.json")
    if not input_file.exists():
        logger.error("Input file not found: %s", input_file)
        print(f"\nInput file not found:\n{input_file}")
        return

    # --------------------------------------------------
    # Create Engine
    # --------------------------------------------------

    engine = LegalKnowledgeGraphEngine()
    try:
        results = engine.process_document(input_file)
    except Exception as e:
        logger.exception(e)
        print("\nAn error occurred.\n")
        traceback.print_exc()
        return

    # --------------------------------------------------
    # Results
    # --------------------------------------------------

    print()

    print("=" * 80)
    print("PROCESS COMPLETED SUCCESSFULLY")
    print("=" * 80)

    document = results["document"]
    graph = results["knowledge_graph"]
    print(f"\nDocument : {document.title}")
    print(f"Clauses  : {document.clause_count}")
    print(f"Nodes    : {graph.node_count}")
    print(f"Edges    : {graph.edge_count}")
    print(f"Entities : {len(results['entities'])}")
    print(f"Relations: {len(results['relations'])}")
    print(f"Dependencies: {len(results['dependencies'])}")

    print("\nGraph Statistics")
    for key, value in results["statistics"].items():
        print(f"  {key:25} : {value}")

    print("\nGenerated Files")
    print("-----------------------------")

    for name, path in results["exports"].items():
        print(f"{name:12} -> {path}")

    print()
    print("Visualization")
    print("-----------------------------")
    for name, path in results["visualization"].items():
        print(f"{name:12} -> {path}")

    print()
    print("=" * 80)
    print("Thank you for using Legal Knowledge Graph.")
    print("=" * 80)


if __name__ == "__main__":
    main()