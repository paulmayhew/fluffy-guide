from typing import Dict, Optional

from app.database.repositories.dependency import DependencyRepository
from app.database.repositories.edge import EdgeRepository
from app.database.repositories.flowchart import FlowchartRepository
from app.database.repositories.node import NodeRepository


class FlowchartService:
    """
    Service for managing flowcharts and their components.
    Coordinates operations across multiple repositories.
    """

    @staticmethod
    async def create_flowchart(flowchart_data: dict) -> Dict:
        """
        Create a new flowchart with its initial nodes and edges.
        """
        # Extract components
        nodes_data = flowchart_data.pop("nodes", [])
        edges_data = flowchart_data.pop("edges", [])
        dependencies_data = flowchart_data.pop("dependencies", [])

        # Create flowchart
        flowchart = await FlowchartRepository.create_flowchart(flowchart_data)

        # Create nodes
        nodes = []
        for node_data in nodes_data:
            node_data["kb_chart_id"] = flowchart.kb_id
            node = await NodeRepository.create_node(node_data)
            nodes.append(node)

        # Create edges
        edges = []
        for edge_data in edges_data:
            edge_data["kb_chart_id"] = flowchart.kb_id
            edge = await EdgeRepository.create_edge(edge_data)
            edges.append(edge)

        # Create dependencies
        dependencies = []
        for dependency_data in dependencies_data:
            dependency_data["kb_chart_id"] = flowchart.kb_id
            dependency = await DependencyRepository.create_dependency(dependency_data)
            dependencies.append(dependency)

        # Return complete flowchart
        return {
            "chart": flowchart,
            "nodes": nodes,
            "edges": edges,
            "dependencies": dependencies
        }

    @staticmethod
    async def get_flowchart(chart_id: int) -> Optional[Dict]:
        """
        Get a complete flowchart with all its components.
        """
        return await FlowchartRepository.get_complete_flowchart(chart_id)

    @staticmethod
    async def update_flowchart(chart_id: int, data: Dict) -> Optional[Dict]:
        """
        Update a flowchart and its components.
        """
        # Extract component updates
        chart_data = {k: v for k, v in data.items()
                      if k not in ["nodes", "edges", "dependencies"]}

        nodes_data = data.get("nodes", [])
        edges_data = data.get("edges", [])
        dependencies_data = data.get("dependencies", [])

        # Update flowchart
        if chart_data:
            await FlowchartRepository.update_flowchart(chart_id, chart_data)

        # Update nodes - requires individual updates
        for node_data in nodes_data:
            node_id = node_data.pop("node_id", None)
            if node_id:
                await NodeRepository.update_node(chart_id, node_id, node_data)

        # Update edges
        for edge_data in edges_data:
            edge_id = edge_data.pop("edge_id", None)
            if edge_id:
                await EdgeRepository.update_edge(chart_id, edge_id, edge_data)

        # Update dependencies
        for dependency_data in dependencies_data:
            dependency_id = dependency_data.pop("dependency_id", None)
            if dependency_id:
                await DependencyRepository.update_dependency(chart_id, dependency_id, dependency_data)

        # Return updated flowchart
        return await FlowchartService.get_flowchart(chart_id)

    @staticmethod
    async def delete_flowchart(chart_id: int) -> bool:
        """
        Delete a flowchart and all its components.
        """
        return await FlowchartRepository.delete_flowchart(chart_id)
