# app/api/api.py
from fastapi import APIRouter

from app.api.routes import flowcharts, nodes, progression

api_router = APIRouter()

# Include sub-routers
api_router.include_router(flowcharts.router, prefix="/flowcharts", tags=["Flowcharts"])
api_router.include_router(nodes.router, prefix="/nodes", tags=["Nodes"])
api_router.include_router(progression.router, prefix="/progression", tags=["Progression"])