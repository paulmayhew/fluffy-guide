from datetime import datetime, timezone
from typing import Optional

import pymongo
from beanie import Document
from pydantic import Field


class KbEdge(Document):
    edge_id: str = Field(...)  # Unique identifier for this edge
    kb_chart_id: int = Field(...)  # Reference to parent flowchart
    source: str = Field(...)  # ID of source node
    target: str = Field(...)  # ID of target node

    # Optional edge styling/properties
    label: Optional[str] = None  # Text to display on the edge
    type: str = Field(default="default")  # Edge type for styling (e.g., "success", "error")
    animated: bool = Field(default=False)  # Whether edge has animation

    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    class Settings:
        name = "KBEdges"
        indexes = [
            [("edge_id", pymongo.ASCENDING)],
            [("kb_chart_id", pymongo.ASCENDING)],
            [("source", pymongo.ASCENDING)],
            [("target", pymongo.ASCENDING)],
            [("kb_chart_id", pymongo.ASCENDING), ("edge_id", pymongo.ASCENDING)]
        ]
