from datetime import datetime 
from typing import Union , Optional , Dict , Any , Literal 
from pydantic import BaseModel , Field , field_validator 

# --- Request Schemas --- 
class ChatRequest(BaseModel):
    """
        Schema For Incoming Chat Requests from the Frontend 
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's natural language prompt about Notion Data ",
        examples=[
            "summarize the page 'MCP Quick Start'",
            "what is feature #4 in the PRD?",
            "create a meeting notes page for today's standup"
        ]

    )
    @field_validator('message')
    @classmethod
    def validate_message(cls,v:str)-> str:
        """
            Validate and clean the user message input.
        """
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty")
        return v
# --- SSE Event Data Models ---- 
class AgentStartData(BaseModel):
    """Data payload for agent start event."""
    status: Literal["started"] = "started"

class ReasoningData(BaseModel):
    """Data payload for agent reasoning/thinking events."""
    thought: str = Field(..., description="Agent's reasoning step or thought process")

class ToolCallData(BaseModel):
    """Data payload for tool call events."""
    tool_name: str = Field(..., description="Name of the tool being called (e.g., 'search')")
    tool_input: Dict[str, Any] = Field(..., description="Input parameters for the tool")

class ToolOutputData(BaseModel):
    """Data payload for tool output events."""
    tool_name: str = Field(..., description="Name of the tool that was called")
    tool_output: str = Field(..., description="Raw output from the tool (JSON string)")

class FinalAnswerData(BaseModel):
    """Data payload for final answer events."""
    answer: str = Field(..., description="Complete answer to user's query")

class ErrorData(BaseModel):
    """Data payload for error events."""
    error: str = Field(..., description="Error message")
    error_type: Optional[str] = Field(None, description="Type/category of error (e.g., 'auth')")

class StreamEndData(BaseModel):
    """Data payload for stream end events."""
    status: Literal["finished"] = "finished"

# ---- SSE Event Wrapper ----
class SSEEvent(BaseModel):
    """Wrapper for Server-Sent Events with proper typing."""
    event: str = Field(..., description="Event type name (e.g., 'reasoning')")
    data: Union[
        AgentStartData,
        ReasoningData,
        ToolCallData,
        ToolOutputData,
        FinalAnswerData,
        ErrorData,
        StreamEndData
    ] = Field(..., description="Event data payload")

    def to_sse_string(self) -> str:
        """Convert to proper SSE format for transmission."""
        return f"event: {self.event}\ndata: {self.data.model_dump_json()}\n\n"

# --- HTTP Response Schemas ---
class HealthCheckResponse(BaseModel):
    """Schema for health check endpoint response."""
    status: Literal["healthy"] = "healthy"
    app_name: str
    version: str = "1.0.0"
    mcp_status: Literal["connected", "disconnected", "error"] = "connected"

class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str = Field(..., description="Error description")
    error_type: Optional[str] = Field(None, description="Type of error")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# --- Exports for easy imports ---
__all__ = [
    "ChatRequest",
    "SSEEvent",
    "AgentStartData",
    "ReasoningData",
    "ToolCallData",
    "ToolOutputData",
    "FinalAnswerData",
    "ErrorData",
    "StreamEndData",
    "HealthCheckResponse",
    "ErrorResponse",
]