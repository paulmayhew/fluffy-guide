from typing import Dict, List

from app.database.repositories.dependency import DependencyRepository
from app.database.repositories.node import NodeRepository
from app.models.node import KbNode


class ProgressionService:
    """
    Service for managing node progression/activation logic.
    """

    @staticmethod
    async def complete_node(chart_id: int, node_id: str) -> Dict:
        """
        Mark a node as completed and activate dependent nodes.
        Returns the completed node and newly activated nodes.
        """
        # Mark node as completed
        node = await NodeRepository.mark_node_complete(chart_id, node_id)
        if not node:
            return {"error": "Node not found"}

        # Process dependencies to activate next nodes
        activated_nodes = await DependencyRepository.process_node_completion(chart_id, node_id)

        return {
            "completed_node": node,
            "activated_nodes": activated_nodes
        }

    @staticmethod
    async def get_active_nodes(chart_id: int) -> List[KbNode]:
        """
        Get all currently active nodes for a flowchart.
        """
        nodes = await NodeRepository.get_nodes_by_chart(chart_id)
        return [node for node in nodes if node.active]

    @staticmethod
    async def reset_flowchart_progress(chart_id: int) -> bool:
        """
        Reset all nodes to their initial state:
        - Starting nodes active, rest inactive
        - All nodes marked as not completed
        """
        nodes = await NodeRepository.get_nodes_by_chart(chart_id)

        for node in nodes:
            # Reset completion status
            node.completed = False

            # Reset active status based on initial configuration
            # Assuming node_id "1" or similar is your starting node
            if node.node_id == "1":  # Adjust based on your starting node ID
                node.active = True
            else:
                node.active = False

            await NodeRepository.update_node(
                chart_id,
                node.node_id,
                {"active": node.active, "completed": node.completed}
            )

        return True
