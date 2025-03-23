from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import os
import os
from dotenv import load_dotenv

server_params = StdioServerParameters(
    command="C://Users//user//AppData//Local//Programs//Python//Python313//python.exe",
    args=[
        "-m",
        "mcp_server_servicenow.cli",
        "--url", "https://dev268377.service-now.com/",
        "--username", "admin",
        "--password", "A72D^ksF$oFc"
    ],
)


# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("MISTRAL_API_KEY")

from langchain.chat_models import init_chat_model
import asyncio

model = init_chat_model("mistral-large-latest", model_provider="mistralai")


async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response_tool = await agent.ainvoke({"messages": "566 + 667"})
            #agent_response__llm = await agent.ainvoke({"messages": "capital of india"})
            print(agent_response_tool)
            print("Next one :")
            #print(agent_response__llm)

# Run the async function
if __name__ == "__main__":
    result = asyncio.run(run_agent())
    print(result)