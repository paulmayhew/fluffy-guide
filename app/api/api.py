# app/api/api.py
from fastapi import APIRouter

from app.api.routes import flowcharts, nodes, progression, flowchart_creation

api_router = APIRouter()

api_router.include_router(flowcharts.router, prefix="/flowcharts", tags=["Flowcharts"])
api_router.include_router(nodes.router, prefix="/nodes", tags=["Nodes"])
api_router.include_router(progression.router, prefix="/progression", tags=["Progression"])
api_router.include_router(flowchart_creation.router, prefix="/flowcharts", tags=["Flowchart Creation"])
