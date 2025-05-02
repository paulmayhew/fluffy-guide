# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings
from app.database.connection import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup: Connect to the database
    await init_db(settings.MONGO_URI)
    yield


# Create FastAPI application
app = FastAPI(
    title="Interactive Flowchart API",
    description="API for managing interactive flowcharts with progressive disclosure",
    version="1.0.0",
    lifespan=lifespan
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
