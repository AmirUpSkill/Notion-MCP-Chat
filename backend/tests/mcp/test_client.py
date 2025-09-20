import asyncio
from app.mcp.client import initialize_mcp_client, get_mcp_client, close_mcp_client

async def test():
    await initialize_mcp_client()
    client = await get_mcp_client()
    print(f"Client created: {client}")
    await close_mcp_client()

if __name__ == "__main__":
    asyncio.run(test())