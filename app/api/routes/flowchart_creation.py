# app/api/routes/flowchart_creation.py

from fastapi import APIRouter, HTTPException, Body

from app.core.utils import serialize_document
from app.database.repositories.edge import EdgeRepository
from app.database.repositories.flowchart import FlowchartRepository
from app.database.repositories.node import NodeRepository
from app.services.mermaid_parser import parse_extended_mermaid

router = APIRouter()


@router.post("/create-from-mermaid", response_model=None)
async def create_flowchart_from_mermaid(
        content: str = Body(..., embed=True)
):
    """
    Create a new flowchart from extended Mermaid format.
    """
    try:
        # Parse the extended Mermaid content
        parsed_data = parse_extended_mermaid(content)

        # Create the flowchart
        chart_data = {
            "kb_id": parsed_data["kb_id"],
            "title": parsed_data["title"],
            "description": parsed_data["description"]
        }

        flowchart = await FlowchartRepository.create_flowchart(chart_data)

        # Now create nodes and edges using the flowchart's ID
        nodes_data = parsed_data.get("nodes", [])
        for node in nodes_data:
            await NodeRepository.create_node(node)

        edges_data = parsed_data.get("edges", [])
        for edge in edges_data:
            await EdgeRepository.create_edge(edge)

        # Get the complete flowchart with all its components
        result = await FlowchartRepository.get_complete_flowchart(flowchart.kb_id)

        # Serialize the result to ensure it can be properly JSON encoded
        serialized_result = serialize_document(result)

        return serialized_result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create flowchart: {str(e)}")
