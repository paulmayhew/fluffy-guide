# app/database/repositories/flowchart_repository.py
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from app.models.dependency import KbDependency
from app.models.edge import KbEdge
from app.models.flowchart import KbChart
from app.models.node import KbNode


class FlowchartRepository:
    """
    Repository for flowchart-related database operations.
    """

    @staticmethod
    async def create_flowchart(chart_data: dict) -> KbChart:
        """Create a new flowchart"""
        # Add timestamps
        chart_data["created_at"] = datetime.now(timezone.utc)
        chart_data["updated_at"] = datetime.now(timezone.utc)

        chart = KbChart(**chart_data)
        await chart.insert()  # Beanie's insert doesn't need parameters
        return chart

    @staticmethod
    async def get_flowchart(chart_id: int) -> Optional[KbChart]:
        """Retrieve a flowchart by ID"""
        return await KbChart.find_one({"kb_id": chart_id})

    @staticmethod
    async def update_flowchart(chart_id: int, data: Dict[str, Any]) -> Optional[KbChart]:
        """Update a flowchart"""
        # Add updated timestamp
        data["updated_at"] = datetime.now(timezone.utc)

        # Find and update
        chart = await KbChart.find_one({"kb_id": chart_id})
        if not chart:
            return None

        for key, value in data.items():
            setattr(chart, key, value)

        await chart.save()
        return chart

    @staticmethod
    async def delete_flowchart(chart_id: int) -> bool:
        await KbNode.find({"kb_chart_id": chart_id}).delete_many()
        await KbEdge.find({"kb_chart_id": chart_id}).delete_many()
        await KbDependency.find({"kb_chart_id": chart_id}).delete_many()

        result = await KbChart.find({"kb_id": chart_id}).delete_many()
        return result.deleted_count > 0

    @staticmethod
    async def get_complete_flowchart(chart_id: int) -> Optional[Dict]:
        """
        Get a flowchart with all its nodes, edges, and dependencies
        """
        chart = await FlowchartRepository.get_flowchart(chart_id)
        if not chart:
            return None

        nodes = await KbNode.find({"kb_chart_id": chart_id}).to_list()
        edges = await KbEdge.find({"kb_chart_id": chart_id}).to_list()
        dependencies = await KbDependency.find({"kb_chart_id": chart_id}).to_list()

        chart_dict = chart.model_dump() if hasattr(chart, "dict") else {"error": "Failed to serialize chart"}
        nodes_list = [node.model_dump() if hasattr(node, "dict") else node for node in nodes]
        edges_list = [edge.model_dump() if hasattr(edge, "dict") else edge for edge in edges]
        dependencies_list = [dep.model_dump() if hasattr(dep, "dict") else dep for dep in dependencies]

        return {
            "chart": chart_dict,
            "nodes": nodes_list,
            "edges": edges_list,
            "dependencies": dependencies_list
        }

    @staticmethod
    async def get_all_flowcharts() -> list:
        """Get all flowcharts without their related data"""
        charts = await KbChart.find_all().to_list()
        return charts
