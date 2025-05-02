# app/api/routes/flowchart_creation.py
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Body

from app.database.repositories.edge import EdgeRepository
from app.database.repositories.flowchart import FlowchartRepository
from app.database.repositories.node import NodeRepository
from app.services.mermaid_parser import parse_extended_mermaid

router = APIRouter()


@router.post("/create-from-mermaid", response_model=Dict[str, Any])
async def create_flowchart_from_mermaid(
        content: str = Body(..., embed=True)
):
    """
    Create a new flowchart from extended Mermaid format.
    """
    try:
        # Parse the extended Mermaid content
        parsed_data = parse_extended_mermaid(content)

        # Extract chart data and fix the structure
        chart_data = parsed_data.get("chart", {})

        # Create the flowchart first
        flowchart = await FlowchartRepository.create_flowchart(chart_data)

        # Now create nodes and edges using the flowchart's ID
        nodes_data = parsed_data.get("nodes", [])
        for node in nodes_data:
            # Update the kb_chart_id to match the created flowchart
            node["kb_chart_id"] = flowchart.kb_id
            await NodeRepository.create_node(node)

        edges_data = parsed_data.get("edges", [])
        for edge in edges_data:
            # Update the kb_chart_id to match the created flowchart
            edge["kb_chart_id"] = flowchart.kb_id
            await EdgeRepository.create_edge(edge)

        # Get the complete flowchart with all its components
        result = await FlowchartRepository.get_complete_flowchart(flowchart.kb_id)

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create flowchart: {str(e)}")
