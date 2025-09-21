from fastapi import APIRouter
from .chat import router as chat_router

# --- Main API v1 router ---
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(chat_router)