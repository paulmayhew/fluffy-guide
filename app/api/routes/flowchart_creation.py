# app/api/routes/flowchart_creation.py
from typing import Dict, Any

from app.services.flowchart import FlowchartService
from app.services.mermaid_parser import parse_extended_mermaid
from fastapi import APIRouter, HTTPException, Body

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

        # Create the flowchart using the existing service
        result = await FlowchartService.create_flowchart(parsed_data)

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create flowchart: {str(e)}")
