# app/dependencies.py
from typing import Dict, Any

from fastapi import HTTPException, status

from app.database.repositories.flowchart import FlowchartRepository
from app.services.flowchart import FlowchartService


# Function to verify flowchart exists
async def valid_flowchart_id(chart_id: int) -> Dict[str, Any]:
    """
    Dependency to check if a flowchart exists and return it.
    Raises 404 if not found.
    """
    flowchart = await FlowchartService.get_flowchart(chart_id)
    if not flowchart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flowchart with ID {chart_id} not found"
        )
    return flowchart


# Function to get database repositories
def get_flowchart_repository():
    """
    Dependency to get the FlowchartRepository.
    This makes it easier to mock repositories for testing.
    """
    return FlowchartRepository()
