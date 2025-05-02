# app/database/connection.py
from typing import List

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.dependency import KbDependency
from app.models.edge import KbEdge
from app.models.flowchart import KbChart
from app.models.node import KbNode


async def init_db(db_url: str):
    client = AsyncIOMotorClient(db_url)

    db = client.knowledge_base

    document_models: List[type] = [KbChart, KbNode, KbEdge, KbDependency]
    await init_beanie(database=db, document_models=document_models)

    return client
