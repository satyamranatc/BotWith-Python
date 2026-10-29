"""
Groq LLM with MCP Tool Support
───────────────────────────────
Connects to two MCP servers:
  • system_actions  — file/folder/app management
  • ObjectFinder    — webcam object detection (YOLO)

The LLM can call any of their tools automatically based on your prompt.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

# ── Paths to MCP server scripts ───────────────────────────────────────────────
_HERE = os.path.dirname(__file__)
SYSTEM_ACTIONS_SERVER = os.path.abspath(os.path.join(_HERE, "system_actions.py"))
VISION_SERVER         = os.path.abspath(os.path.join(_HERE, "objectFinder.py"))

# ── Groq LLM ─────────────────────────────────────────────────────────────────
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
)


# ── MCP client factory ────────────────────────────────────────────────────────
def _make_mcp_client() -> MultiServerMCPClient:
    """Build a client connected to all MCP tool servers."""
    return MultiServerMCPClient(
        {
            "system_actions": {
                "command": sys.executable,
                "args": [SYSTEM_ACTIONS_SERVER],
                "transport": "stdio",
            },
            "ObjectFinder": {
                "command": sys.executable,
                "args": [VISION_SERVER],
                "transport": "stdio",
            },
        }
    )


# ── Core async function ───────────────────────────────────────────────────────
async def ask_groq_async(prompt: str, max_steps: int = 5) -> str:
    """
    Send a prompt to Groq. The LLM can call MCP tools in a loop
    (up to max_steps rounds) until it has a final text answer.
    """
    client = _make_mcp_client()
    tools = await client.get_tools()
    tools_by_name = {tool.name: tool for tool in tools}

    llm_with_tools = llm.bind_tools(tools)
    messages = [HumanMessage(content=prompt)]

    for _ in range(max_steps):
        response = await llm_with_tools.ainvoke(messages)
        messages.append(response)

        # No tool calls → LLM is done, return its answer
        if not response.tool_calls:
            return response.content

        # Execute every tool the LLM requested
        for call in response.tool_calls:
            name    = call["name"]
            args    = call["args"]
            call_id = call["id"]

            if name in tools_by_name:
                try:
                    result = await tools_by_name[name].ainvoke(args)
                except Exception as e:
                    result = f"Error running '{name}': {e}"
            else:
                result = f"Unknown tool: '{name}'"

            messages.append(ToolMessage(content=str(result), tool_call_id=call_id))

    # Safety fallback if max_steps is reached
    return response.content or "Done."


# ── Sync wrapper (for use outside async code) ─────────────────────────────────
def ask_groq(prompt: str) -> str:
    """Synchronous wrapper around ask_groq_async."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # We're already inside an event loop (e.g. Jupyter / voice thread)
        return asyncio.run_coroutine_threadsafe(ask_groq_async(prompt), loop).result()
    else:
        return asyncio.run(ask_groq_async(prompt))


# ── Quick self-test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    test = "Create a folder named jarvis_test_mcp and inside it create a file called hello.py"
    print(f"Prompt : {test}")
    print(f"Answer : {ask_groq(test)}")
