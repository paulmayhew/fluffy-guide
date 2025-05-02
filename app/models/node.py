from datetime import datetime, timezone
from typing import Optional, List

import pymongo
from beanie import Document
from pydantic import Field, BaseModel


class Position(BaseModel):
    x: float
    y: float


class NodeContent(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = ""
    actions: Optional[str] = None
    questions: Optional[List[str]] = Field(default_factory=list)


class KbNode(Document):
    node_id: str = Field(...)  # Unique identifier within the flowchart
    kb_chart_id: int = Field(...)  # Reference to parent flowchart
    type: str = Field(default="custom")  # Node type (for custom styling/behavior)
    position: Position  # X,Y coordinates in the flowchart
    content: NodeContent  # The actual information to display
    active: bool = Field(default=False)  # Whether node is initially clickable
    completed: bool = Field(default=False)  # Whether user has marked as done

    activates_nodes: List[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    class Settings:
        name = "KBNodes"
        indexes = [
            [("node_id", pymongo.ASCENDING)],
            [("kb_chart_id", pymongo.ASCENDING)],
            [("kb_chart_id", pymongo.ASCENDING), ("node_id", pymongo.ASCENDING)]
        ]
