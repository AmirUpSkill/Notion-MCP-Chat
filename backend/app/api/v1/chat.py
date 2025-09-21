from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
from app.schemas.chat import ChatRequest
from app.services.chat_service import process_chat_request

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream chat responses using Server-Sent Events (SSE).
    
    - **message**: User's natural language query.
    - **enable_notion**: Toggle Notion MCP integration (default: true).
    
    Returns SSE stream with events like agent_start, reasoning, tool_call, final_answer, stream_end.
    """
    async def generate_events():
        async for event in process_chat_request(request):
            yield {
                "event": event.event,
                "data": event.data.model_dump()
            }
    
    return EventSourceResponse(
        generate_events(),
        ping=15000,  
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
