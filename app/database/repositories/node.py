from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from app.models.node import KbNode


class NodeRepository:
    @staticmethod
    async def create_node(node_data: dict) -> KbNode:
        """Create a new node"""
        node_data["created_at"] = datetime.now(timezone.utc)
        node_data["updated_at"] = datetime.now(timezone.utc)

        node = KbNode(**node_data)
        await node.insert()
        return node

    @staticmethod
    async def get_node(kb_chart_id: int, node_id: str) -> Optional[KbNode]:
        """Get a specific node from a flowchart"""
        return await KbNode.find_one({"kb_chart_id": kb_chart_id, "node_id": node_id})

    @staticmethod
    async def get_nodes_by_chart(kb_chart_id: int) -> List[KbNode]:
        """Get all nodes for a specific flowchart"""
        return await KbNode.find({"kb_chart_id": kb_chart_id}).to_list()

    @staticmethod
    async def update_node(kb_chart_id: int, node_id: str, data: Dict[str, Any]) -> Optional[KbNode]:
        """Update a node"""
        data["updated_at"] = datetime.now(timezone.utc)

        node = await NodeRepository.get_node(kb_chart_id, node_id)
        if not node:
            return None

        for key, value in data.items():
            setattr(node, key, value)

        await node.save()
        return node

    @staticmethod
    async def delete_node(kb_chart_id: int, node_id: str) -> bool:
        """Delete a node"""
        result = await KbNode.find_one({"kb_chart_id": kb_chart_id, "node_id": node_id})
        if result:
            await result.delete()
            return True
        return False

    @staticmethod
    async def mark_node_complete(kb_chart_id: int, node_id: str) -> Optional[KbNode]:
        """Mark a node as completed and return nodes that should be activated"""
        node = await NodeRepository.get_node(kb_chart_id, node_id)
        if not node:
            return None

        # Update completion status
        node.completed = True
        node.updated_at = datetime.now(timezone.utc)
        await node.save()

        # Activate dependent nodes based on this node's activates_nodes list
        if node.activates_nodes:
            for activate_id in node.activates_nodes:
                target_node = await NodeRepository.get_node(kb_chart_id, activate_id)
                if target_node and not target_node.active:
                    target_node.active = True
                    target_node.updated_at = datetime.now(timezone.utc)
                    await target_node.save()

        return node
