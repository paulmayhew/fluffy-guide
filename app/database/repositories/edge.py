from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from app.models.edge import KbEdge


class EdgeRepository:
    @staticmethod
    async def create_edge(edge_data: dict) -> KbEdge:
        """Create a new edge between nodes"""
        edge_data["created_at"] = datetime.now(timezone.utc)
        edge_data["updated_at"] = datetime.now(timezone.utc)

        edge = KbEdge(**edge_data)
        await edge.insert()
        return edge

    @staticmethod
    async def get_edge(kb_chart_id: int, edge_id: str) -> Optional[KbEdge]:
        """Get a specific edge"""
        return await KbEdge.find_one({"kb_chart_id": kb_chart_id, "edge_id": edge_id})

    @staticmethod
    async def get_edges_by_chart(kb_chart_id: int) -> List[KbEdge]:
        """Get all edges for a specific flowchart"""
        return await KbEdge.find({"kb_chart_id": kb_chart_id}).to_list()

    @staticmethod
    async def get_edges_by_source(kb_chart_id: int, source_id: str) -> List[KbEdge]:
        """Get all edges starting from a specific node"""
        return await KbEdge.find({"kb_chart_id": kb_chart_id, "source": source_id}).to_list()

    @staticmethod
    async def update_edge(kb_chart_id: int, edge_id: str, data: Dict[str, Any]) -> Optional[KbEdge]:
        """Update an edge"""
        data["updated_at"] = datetime.now(timezone.utc)

        edge = await EdgeRepository.get_edge(kb_chart_id, edge_id)
        if not edge:
            return None

        for key, value in data.items():
            setattr(edge, key, value)

        await edge.save()
        return edge

    @staticmethod
    async def delete_edge(kb_chart_id: int, edge_id: str) -> bool:
        """Delete an edge"""
        result = await KbEdge.find_one({"kb_chart_id": kb_chart_id, "edge_id": edge_id})
        if result:
            await result.delete()
            return True
        return False
