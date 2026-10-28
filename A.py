import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
)

# Locate B.py in the same directory as A.py
server_path = Path(__file__).parent / "B.py"


async def askAi(q):
    print("Connecting to MCP server...")

    client = MultiServerMCPClient({
        "MySkills": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [str(server_path)],
        }
    })

    tools = await client.get_tools()

    print("Connected successfully!")
    print("Available tools:", [tool.name for tool in tools])

    agent = create_react_agent(llm, tools)

    response = await agent.ainvoke({
        "messages": [HumanMessage(content=q)]
    })

    print("\nAI:", response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(askAi("Hi"))
