from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from typing import cast
import os
from dotenv import load_dotenv
import chainlit as cl
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langgraph.prebuilt import create_react_agent
from langchain.schema.runnable import RunnableLambda

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("MISTRAL_API_KEY")

from langchain.chat_models import init_chat_model

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

async def init_mcp_tools():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()  # Establish the connection
            tools = await load_mcp_tools(session)  # Load available MCP tools
            return tools

@cl.on_chat_start
async def on_chat_start():
    model = init_chat_model("mistral-large-latest", model_provider="mistralai")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an assistant that uses all tools at your disposal",
            ),
            ("human", "{question}"),
        ]
    )

    tools = await init_mcp_tools()
    agent = create_react_agent(model, tools)


    def extract_text(response):
        if isinstance(response, dict) and "output" in response:
         return response["output"]
        return str(response)  # Fallback to string conversion


    runnable = prompt | agent | RunnableLambda(extract_text)
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cast(Runnable, cl.user_session.get("runnable"))  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()

