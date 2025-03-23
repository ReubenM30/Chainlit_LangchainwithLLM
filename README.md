**langchain_mistral.py** - Chainlit documentation example that uses langchain to connect to LLM models <br>
**math_server.py** - Local MCP server needed in app.py <br>
**app.py** - POC to check if langchain can read mcp tools and internally use the langgpraph agent to decide between calling LLM and Tool. It is calling the Math MCP tool positively <br>
**app2.py** - Chainlit integration to langchain + tools ( Loaded with the ServiceNow MCP tool, however, agent is not calling it) <br>
**app3.py** - Same thing as above but without chainlit ( just manually calling to debug agent calling tool part ) <br>
