from contextlib import asynccontextmanager

import uvicorn
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ecrm_api import __version__
from ecrm_api.config import origins
from ecrm_api.core.config import settings
from ecrm_api.routes import api_router

@asynccontextmanager
async def app_init(app: FastAPI):
    app.include_router(api_router, prefix=settings.api_v1_str)
    yield


app = FastAPI(
    title=settings.project_name,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    lifespan=app_init,
)

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": f"eCRM API version {__version__.__version__}"}

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("ecrm_api.main:app", host=settings.server_uri, port=int(settings.server_port), reload=True)