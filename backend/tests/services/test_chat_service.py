import asyncio
from app.services.chat_service import process_chat_request
from app.schemas.chat import ChatRequest
from app.mcp.client import initialize_mcp_client, close_mcp_client

async def test_notion_enabled():
    """Test with Notion enabled—verify streaming events."""
    await initialize_mcp_client()
    
    request = ChatRequest(message="summarize the page 'MCP Quick Start'", enable_notion=True)
    
    print("🧪 Testing with Notion enabled...")
    print("=" * 60)
    
    events = []
    async for event in process_chat_request(request):
        print(event.to_sse_string())
        events.append(event)
    
    # Assertions (reasoning/tool events are optional depending on agent behavior)
    assert len(events) >= 3, f"Expected ≥3 events, got {len(events)}" 
    assert any(e.event == "agent_start" for e in events), "Missing agent_start event"
    assert any(e.event == "final_answer" for e in events), "Missing final answer"
    assert any(e.event == "stream_end" for e in events), "Missing stream_end event"
    
    print(f"✅ Enabled test passed: {len(events)} events streamed.")
    await close_mcp_client()

async def test_notion_disabled():
    """Test with Notion disabled—verify basic LLM fallback."""
    request = ChatRequest(message="What is MCP?", enable_notion=False)
    
    print("\n🧪 Testing with Notion disabled...")
    print("=" * 60)
    
    events = []
    async for event in process_chat_request(request):
        print(event.to_sse_string())
        events.append(event)
    
    # Expect 4 events: start, reasoning, final_answer, end
    assert len(events) == 4, f"Expected 4 events (start + reasoning + answer + end), got {len(events)}"
    assert any(e.event == "agent_start" for e in events), "Missing agent_start event"
    assert any(e.event == "final_answer" for e in events), "Missing final answer"
    assert any(e.event == "stream_end" for e in events), "Missing stream_end event"
    
    print("✅ Disabled test passed.")

async def main():
    print("🚀 Starting simplified service tests...\n")
    await test_notion_enabled()
    await test_notion_disabled()
    print("\n🎉 All tests passed!")

if __name__ == "__main__":
    asyncio.run(main())