import logging
from mcp_use import MCPAgent, MCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from ..core.config import settings

logger = logging.getLogger(__name__)

def create_agent(client: MCPClient) -> MCPAgent:
    """
        Factory Function to create a configured MCPAgent instance 
        
        Args:
            Client : The pre-initialized MCPClient singleton 
        Returns:
            A fullly configured MCPAgent ready for execution 
    """
    logger.info("🧠 Creating MCPAgent...")
    try:
        # --- Step 1 : Initialize the LLM (Gemini 2.5 Pro ) ---
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            google_api_key=settings.gemini_api,
            temperature=0.7,
        )
        # --- Step 2 : Create the Agent Instance ---- 
        agent = MCPAgent(
            llm=llm,
            client=client,
            max_steps=30,
        )
        logger.info("✅ MCPAgent created successfully.")
        return agent
    except Exception as e:
        logger.error(f"❌ Failed to create MCPAgent: {e}")
        raise RuntimeError(f"MCPAgent creation failed: {e}")