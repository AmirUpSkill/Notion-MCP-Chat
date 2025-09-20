import asyncio
from app.mcp.client import initialize_mcp_client, get_mcp_client
from app.mcp.agent import create_agent

async def test():
    await initialize_mcp_client()
    client = await get_mcp_client()
    agent = create_agent(client)
    print(f"Agent created: {agent}")
    print("Running a test query...")
    result = await agent.run("Say hello from Notion MCP!")
    print(f"Test result: {result}")

if __name__ == "__main__":
    asyncio.run(test())