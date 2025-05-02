# app/api/routes/nodes.py
from typing import Dict, List

from fastapi import APIRouter, HTTPException, status

from app.database.repositories.node import NodeRepository
from app.models.node import KbNode

router = APIRouter()


@router.post("/", response_model=KbNode, status_code=status.HTTP_201_CREATED)
async def create_node(node_data: Dict):
    """Create a new node in a flowchart"""
    result = await NodeRepository.create_node(node_data)
    return result


@router.get("/{chart_id}", response_model=List[KbNode])
async def get_nodes_by_chart(chart_id: int):
    """Get all nodes for a specific flowchart"""
    nodes = await NodeRepository.get_nodes_by_chart(chart_id)
    return nodes


@router.get("/{chart_id}/{node_id}", response_model=KbNode)
async def get_node(chart_id: int, node_id: str):
    """Get a specific node"""
    node = await NodeRepository.get_node(chart_id, node_id)
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
    return node


@router.put("/{chart_id}/{node_id}", response_model=KbNode)
async def update_node(chart_id: int, node_id: str, node_data: Dict):
    """Update a node"""
    result = await NodeRepository.update_node(chart_id, node_id, node_data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
    return result


@router.delete("/{chart_id}/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_node(chart_id: int, node_id: str):
    """Delete a node"""
    deleted = await NodeRepository.delete_node(chart_id, node_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
