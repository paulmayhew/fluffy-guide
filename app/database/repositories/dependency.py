from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from app.models.dependency import KbDependency
from app.models.node import KbNode


class DependencyRepository:
    @staticmethod
    async def create_dependency(dependency_data: dict) -> KbDependency:
        """Create a new dependency rule"""
        dependency_data["created_at"] = datetime.now(timezone.utc)
        dependency_data["updated_at"] = datetime.now(timezone.utc)

        dependency = KbDependency(**dependency_data)
        await dependency.insert()
        return dependency

    @staticmethod
    async def get_dependency(kb_chart_id: int, dependency_id: str) -> Optional[KbDependency]:
        """Get a specific dependency"""
        return await KbDependency.find_one({"kb_chart_id": kb_chart_id, "dependency_id": dependency_id})

    @staticmethod
    async def get_dependencies_by_chart(kb_chart_id: int) -> List[KbDependency]:
        """Get all dependencies for a specific flowchart"""
        return await KbDependency.find({"kb_chart_id": kb_chart_id}).to_list()

    @staticmethod
    async def get_dependencies_by_source(kb_chart_id: int, source_node_id: str) -> List[KbDependency]:
        """Get all dependencies triggered by a specific node"""
        return await KbDependency.find({"kb_chart_id": kb_chart_id, "source_node_id": source_node_id}).to_list()

    @staticmethod
    async def process_node_completion(kb_chart_id: int, node_id: str) -> List[KbNode]:
        """
        Process dependencies when a node is completed.
        Returns a list of nodes that were activated.
        """
        # Find dependencies where this node is the source
        dependencies = await DependencyRepository.get_dependencies_by_source(kb_chart_id, node_id)

        activated_nodes = []

        # Activate target nodes
        for dependency in dependencies:
            for target_id in dependency.target_node_ids:
                # Find the target node
                target_node = await KbNode.find_one({"kb_chart_id": kb_chart_id, "node_id": target_id})

                if target_node and not target_node.active:
                    # Activate the node
                    target_node.active = True
                    target_node.updated_at = datetime.now(timezone.utc)
                    await target_node.save()

                    activated_nodes.append(target_node)

        return activated_nodes
