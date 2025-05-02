from datetime import datetime, timezone
from typing import List

import pymongo
from beanie import Document
from pydantic import Field


class KbDependency(Document):
    dependency_id: str = Field(...)  # Unique identifier for this dependency
    kb_chart_id: int = Field(...)  # Reference to parent flowchart

    # The node that triggers this dependency
    source_node_id: str = Field(...)

    # The nodes that should be activated when source node is completed
    target_node_ids: List[str] = Field(...)

    # Optional condition - could be simple "completed" or more complex logic
    condition: str = Field(default="completed")

    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    class Settings:
        name = "KBDependencies"
        indexes = [
            [("dependency_id", pymongo.ASCENDING)],
            [("kb_chart_id", pymongo.ASCENDING)],
            [("source_node_id", pymongo.ASCENDING)],
            [("kb_chart_id", pymongo.ASCENDING), ("source_node_id", pymongo.ASCENDING)]
        ]
