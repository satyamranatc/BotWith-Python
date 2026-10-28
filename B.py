from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MySkills")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers and return their sum."""
    return a + b


if __name__ == "__main__":
    mcp.run(transport="stdio")