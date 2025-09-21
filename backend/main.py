from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1.endpoints import api_router
from app.core.config import settings
from app.mcp.client import initialize_mcp_client, close_mcp_client
from app.schemas.chat import HealthCheckResponse
import logging


logging.basicConfig(level=getattr(logging, settings.log_level))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    App lifespan: Initialize MCP client on startup, close on shutdown.
    """
    # ---  Startup ----
    await initialize_mcp_client()
    yield
    # ---  Shutdown ----
    await close_mcp_client()

app = FastAPI(
    title=settings.app_name,
    description="Notion MCP Chat Backend",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify the app and MCP connection.
    """
    return HealthCheckResponse(
        app_name=settings.app_name,
        mcp_status="connected" 
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )