# app/api/routes/progression.py
from typing import Dict, List

from fastapi import APIRouter, HTTPException, status

from app.models.node import KbNode
from app.services.progression import ProgressionService

router = APIRouter()


@router.post("/{chart_id}/complete/{node_id}", response_model=Dict)
async def complete_node(chart_id: int, node_id: str):
    """
    Mark a node as completed and activate dependent nodes.
    Returns the completed node and newly activated nodes.
    """
    result = await ProgressionService.complete_node(chart_id, node_id)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["error"]
        )
    return result


@router.get("/{chart_id}/active", response_model=List[KbNode])
async def get_active_nodes(chart_id: int):
    """Get all currently active nodes for a flowchart"""
    nodes = await ProgressionService.get_active_nodes(chart_id)
    return nodes


@router.post("/{chart_id}/reset", status_code=status.HTTP_200_OK)
async def reset_progress(chart_id: int):
    """Reset flowchart progress to initial state"""
    success = await ProgressionService.reset_flowchart_progress(chart_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flowchart not found"
        )
    return {"message": "Progress reset successfully"}
