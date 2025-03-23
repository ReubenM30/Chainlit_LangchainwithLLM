langchain_mistral.py - Chainlit documentation example that uses langchain to connect to LLM models
math_server.py - Local MCP server needed in app.py
app.py - POC to check if langchain can read mcp tools and internally use the langgpraph agent to decide between calling LLM and Tool.
app2.py - Chainlit integration to langchain + tools ( Loaded with the ServiceNow MCP tool, however, agent is not calling it)
app3.py - Same thing as above but without chainlit ( just manually calling to debug agent calling tool part )
