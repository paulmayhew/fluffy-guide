import json
import re
from typing import Dict, List, Tuple, Any


def parse_extended_mermaid(content: str) -> Dict[str, Any]:
    """Parse an extended Mermaid flowchart with content metadata."""

    # Split the content into sections
    flowchart_match = re.search(r'%%FLOWCHART\n(.*?)(?=%%|$)', content, re.DOTALL)
    dependencies_match = re.search(r'%%DEPENDENCIES\n(.*?)(?=%%|$)', content, re.DOTALL)
    content_match = re.search(r'%%CONTENT\n(.*?)(?=%%|$)', content, re.DOTALL)

    if not flowchart_match or not dependencies_match or not content_match:
        raise ValueError("Invalid format: missing required sections")

    flowchart_text = flowchart_match.group(1).strip()
    dependencies_text = dependencies_match.group(1).strip()
    content_json = content_match.group(1).strip()

    # Parse the flowchart structure (extract nodes and edges)
    node_data, edges = parse_mermaid_flowchart(flowchart_text)
    nodes = node_data["nodes"]
    active_nodes = node_data["active_nodes"]

    # Parse dependencies
    dependencies = parse_dependencies(dependencies_text)

    # Parse content JSON
    try:
        content_data = json.loads(content_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in content section: {e}")

    kb_chart_id = generate_chart_id()
    node_ids = list(nodes.keys())

    processed_nodes = []
    for node_id, node_info in nodes.items():
        if node_id not in content_data.get('nodes', {}):
            raise ValueError(f"Missing content for node: {node_id}")

        node_content = content_data['nodes'][node_id]

        position = extract_position(node_id, node_ids)

        # Create node object
        processed_node = {
            "node_id": node_id,
            "kb_chart_id": kb_chart_id,
            "type": "custom",
            "position": position,
            "content": {
                "title": node_content.get("title", ""),
                "description": node_content.get("description", ""),
                "actions": node_content.get("actions"),
                "questions": node_content.get("questions", [])
            },
            "active": node_id in active_nodes,  # Set active flag based on Mermaid class
            "completed": False,
            "activates_nodes": dependencies.get(node_id, [])
        }

        processed_nodes.append(processed_node)

    # Process edges
    processed_edges = []
    for edge in edges:
        processed_edge = {
            "edge_id": f"e{edge['source']}-{edge['target']}",
            "kb_chart_id": kb_chart_id,
            "source": edge["source"],
            "target": edge["target"]
        }
        processed_edges.append(processed_edge)

    # Create the final structure
    result = {
        "chart": {
            "kb_id": kb_chart_id,
            "title": content_data.get("title", "Flowchart"),
            "description": content_data.get("description", "")
        },
        "nodes": processed_nodes,
        "edges": processed_edges
    }

    return result


def parse_mermaid_flowchart(flowchart_text: str) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
    """Parse a Mermaid flowchart to extract nodes and edges."""
    nodes = {}
    edges = []
    active_nodes = []

    # Extract nodes and edges from flowchart text
    node_pattern = r'(\w+)\[(.*?)\]'
    edge_pattern = r'(\w+)\s*-->\s*(\w+)'
    class_pattern = r'class\s+(\w+)\s+(\w+)'

    # Find all nodes
    for match in re.finditer(node_pattern, flowchart_text):
        node_id = match.group(1)
        node_label = match.group(2)
        nodes[node_id] = {"label": node_label}

    # Find all edges
    for match in re.finditer(edge_pattern, flowchart_text):
        source = match.group(1)
        target = match.group(2)
        edges.append({"source": source, "target": target})

    # Find active nodes
    for match in re.finditer(class_pattern, flowchart_text):
        node_id = match.group(1)
        class_name = match.group(2)
        if class_name == "active":
            active_nodes.append(node_id)

    active_node_list = active_nodes.copy()

    return {"nodes": nodes, "active_nodes": active_node_list}, edges


def parse_dependencies(dependencies_text: str) -> Dict[str, List[str]]:
    """Parse the dependencies section."""
    dependencies = {}

    for line in dependencies_text.strip().split('\n'):
        if not line.strip():
            continue

        parts = line.strip().split(':')
        if len(parts) != 2:
            continue

        sources = parts[0].split(',')
        targets = parts[1].split(',')

        for source in sources:
            dependencies[source.strip()] = [t.strip() for t in targets]

    return dependencies


def extract_position(node_id: str, nodes_list: List[str]) -> Dict[str, float]:
    """
    Extract position from Mermaid data or assign defaults.
    Takes a list of node IDs rather than the nodes dictionary.
    """
    # Simple grid layout algorithm
    index = nodes_list.index(node_id) if node_id in nodes_list else 0

    # Calculate position in a grid-like layout
    columns = 3  # Number of columns in the grid
    x_spacing = 300  # Horizontal spacing between nodes
    y_spacing = 200  # Vertical spacing between nodes

    x = 200 + (index % columns) * x_spacing
    y = 100 + (index // columns) * y_spacing

    return {
        "x": float(x),
        "y": float(y)
    }


def generate_chart_id() -> int:
    import time
    return int(time.time())
