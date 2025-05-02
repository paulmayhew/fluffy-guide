# app/api/routes/flowcharts.py
from typing import Dict, Any, List

from beanie.odm.fields import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from pydantic import PlainSerializer
from typing_extensions import Annotated

from app.database.repositories.flowchart import FlowchartRepository
from app.models.flowchart import KbCreate
from app.services.flowchart import FlowchartService

router = APIRouter()

SerializablePydanticObjectId = Annotated[
    PydanticObjectId,
    PlainSerializer(lambda oid: str(oid))
]


@router.post("/", response_model=Dict, status_code=status.HTTP_201_CREATED)
async def create_flowchart(flowchart: KbCreate):
    """Create a new flowchart with nodes and edges"""
    result = await FlowchartService.create_flowchart(flowchart.model_dump())
    return result


@router.get("/{chart_id}", response_model=Dict)
async def get_flowchart(chart_id: int):
    """Get a complete flowchart with all components"""
    result = await FlowchartService.get_flowchart(chart_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flowchart not found"
        )
    return result


@router.get("/", response_model=List[Dict])
async def get_all_flowcharts():
    """Get all flowcharts"""
    charts = await FlowchartRepository.get_all_flowcharts()

    serialized_charts = []
    for chart in charts:
        # Convert to dict and then handle ObjectId fields
        chart_dict = chart.model_dump()
        # Recursively convert any PydanticObjectId to string
        serialized_charts.append(_convert_objectids(chart_dict))

    return serialized_charts


@router.put("/{chart_id}", response_model=Dict)
async def update_flowchart(chart_id: int, flowchart_data: Dict[str, Any]):
    """Update a flowchart and its components"""
    result = await FlowchartService.update_flowchart(chart_id, flowchart_data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flowchart not found"
        )
    return result


@router.delete("/{chart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flowchart(chart_id: int):
    """Delete a flowchart and all its components"""
    deleted = await FlowchartService.delete_flowchart(chart_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flowchart not found"
        )


# Helper function to recursively convert ObjectIds to strings
def _convert_objectids(obj):
    if isinstance(obj, dict):
        return {k: _convert_objectids(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_objectids(item) for item in obj]
    elif isinstance(obj, PydanticObjectId):
        return str(obj)
    else:
        return obj
