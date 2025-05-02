from datetime import datetime, timezone
from typing import Optional, List

import pymongo
from beanie import Document
from pydantic import Field, BaseModel


class KbID(BaseModel):
    kb_id: int = Field(..., alias='kb_id')


class KbChart(Document):
    kb_id: int = Field(...)
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = ""
    nodes: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    class Settings:
        name = "KBCharts"
        indexes = [
            [("title", pymongo.TEXT)],
            [("kb_id", pymongo.ASCENDING)]
        ]
        keep_nulls = False


class KbCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    nodes: List[str] = Field(default_factory=list)


class KbResponse(BaseModel):
    kb_id: KbID = Field(default_factory=KbID)
    title: str
    description: Optional[str] = ""
    nodes: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
