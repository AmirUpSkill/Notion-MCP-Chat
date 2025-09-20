import logging
from typing import AsyncGenerator, Dict, Any
from app.schemas.chat import (
    SSEEvent, ChatRequest,
    AgentStartData, ReasoningData, ToolCallData, ToolOutputData,
    FinalAnswerData, ErrorData, StreamEndData
)
from app.mcp.client import get_mcp_client
from app.mcp.agent import create_agent
from app.core.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI

logger = logging.getLogger(__name__)

async def process_chat_request(request: ChatRequest) -> AsyncGenerator[SSEEvent, None]:
    """
    Process a chat request with direct agent streaming.
    Args:
        request (ChatRequest): The chat request with message and Notion toggle.
    Yields:
        SSEEvent: Server-Sent Events for real-time UI updates.
    """
    yield SSEEvent(event="agent_start", data=AgentStartData())
    
    try:
        if request.enable_notion:
            logger.info("🧠 Starting full MCP agent mode...")
            client = await get_mcp_client()
            agent = create_agent(client)
            
            # ----  Direct streaming from agent chunks ----
            final_parts = []  
            async for chunk in agent.stream(request.message):
                if isinstance(chunk, dict):
                    #  ---- Parse reasoning from messages ----
                    messages = chunk.get("messages", [])
                    for msg in messages:
                        content_full = msg.get("content", "")
                        content = content_full.lower()
                        # ----  Stream reasoning if present ----
                        if "reasoning" in content or "thought" in content:
                            thought = content_full.strip()
                            if thought:
                                yield SSEEvent(event="reasoning", data=ReasoningData(thought=thought))
                        # --- Accumulate assistant outputs as potential final answer parts ---- 
                        role = (msg.get("role") or "").lower()
                        if role in {"assistant", "ai", "output"} and content_full:
                            final_parts.append(content_full.strip())
                    
                    # ---- Parse tool calls from actions ----
                    actions = chunk.get("actions", [])
                    for action in actions:
                        tool_name = action.get("tool", "unknown")
                        tool_input = action.get("input", {})
                        yield SSEEvent(event="tool_call", data=ToolCallData(tool_name=tool_name, tool_input=tool_input))
                    
                    # ----  Parse tool outputs from steps ---- 
                    steps = chunk.get("steps", [])
                    for step in steps:
                        tool_name = step.get("tool", "unknown")
                        tool_output = str(step.get("output", ""))
                        yield SSEEvent(event="tool_output", data=ToolOutputData(tool_name=tool_name, tool_output=tool_output))
                    
                    # ---- Accumulate final output ----
                    if "final_output" in chunk:
                        final_parts.append(str(chunk["final_output"]))
            
            # ----  Yield final answer ----
            final_answer = " ".join(final_parts).strip()
            if not final_answer:
                try:
                    final_answer = await agent.run(request.message)
                except Exception as e:
                    logger.warning(f"Fallback run() failed to produce final answer: {e}")
                    final_answer = "Agent completed successfully."
            yield SSEEvent(event="final_answer", data=FinalAnswerData(answer=final_answer))
            logger.info("✅ Full MCP agent mode completed.")
        else:
            # ---  Fallback: Basic LLM Call ----
            logger.info("💬 Using basic LLM mode (Notion disabled)")
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=settings.gemini_api,
                temperature=0.7,
            )
            yield SSEEvent(event="reasoning", data=ReasoningData(thought=f"Processing: {request.message}"))
            response = await llm.ainvoke(request.message)
            yield SSEEvent(event="final_answer", data=FinalAnswerData(answer=response.content or "No response generated."))
    
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        yield SSEEvent(event="error", data=ErrorData(error=str(e), error_type=type(e).__name__))
    
    finally:
        yield SSEEvent(event="stream_end", data=StreamEndData())