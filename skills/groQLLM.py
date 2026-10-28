import os
import sys
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

# Path to the MCP server script
MCP_SERVER_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "system_actions.py")
)

# Initialize ChatGroq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
)


def _get_mcp_client() -> MultiServerMCPClient:
    """Create a MultiServerMCPClient connected to the system_actions MCP server."""
    return MultiServerMCPClient(
        {
            "system_actions": {
                "command": sys.executable,
                "args": [MCP_SERVER_PATH],
                "transport": "stdio",
            }
        }
    )


async def ask_groq_async(prompt: str, max_steps: int = 5) -> str:
    """Query Groq with MCP tool support. Supports multi-step tool calls."""
    client = _get_mcp_client()
    tools = await client.get_tools()
    tools_map = {tool.name: tool for tool in tools}

    llm_with_tools = llm.bind_tools(tools)
    messages = [HumanMessage(content=prompt)]

    for _ in range(max_steps):
        response = await llm_with_tools.ainvoke(messages)
        messages.append(response)

        # If the LLM didn't request any tools, return its text response
        if not response.tool_calls:
            return response.content

        # Execute each requested tool call via MCP
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            if tool_name in tools_map:
                try:
                    tool_output = await tools_map[tool_name].ainvoke(tool_args)
                except Exception as e:
                    tool_output = f"Error executing tool {tool_name}: {e}"
            else:
                tool_output = f"Tool '{tool_name}' not found."

            messages.append(
                ToolMessage(content=str(tool_output), tool_call_id=tool_id)
            )

    # Fallback if loop ends
    return response.content or "Completed actions successfully."


def ask_groq(prompt: str) -> str:
    """Synchronous wrapper for ask_groq_async to maintain backward compatibility."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        return asyncio.run_coroutine_threadsafe(
            ask_groq_async(prompt), loop
        ).result()
    else:
        return asyncio.run(ask_groq_async(prompt))


if __name__ == "__main__":
    test_prompt = "Create a folder named jarvis_test_mcp and create a file inside it called test.py"
    print(f"Testing Prompt: {test_prompt}")
    answer = ask_groq(test_prompt)
    print("Response:\n", answer)
