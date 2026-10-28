import os
import sys
import subprocess
from mcp.server.fastmcp import FastMCP

BASE_DIR = os.path.abspath("./JarvisPlayGround")

# Initialize MCP Server
mcp = FastMCP("Jarvis-System-Actions")


def ensure_base_dir():
    """Ensure the base workspace folder exists."""
    os.makedirs(BASE_DIR, exist_ok=True)


@mcp.tool()
def start_app(app_name: str) -> str:
    """Launch a Python script using the active python interpreter."""
    try:
        subprocess.Popen([sys.executable, app_name])
        return f"Successfully started {app_name}."
    except Exception as e:
        return f"Failed to start {app_name}: {e}"


@mcp.tool()
def make_folder(folder_name: str) -> str:
    """Create a directory inside BASE_DIR."""
    ensure_base_dir()
    target_path = os.path.join(BASE_DIR, folder_name)
    os.makedirs(target_path, exist_ok=True)
    return f"Folder created successfully at: {target_path}"


@mcp.tool()
def make_file(folder_name: str, file_name: str) -> str:
    """Create an empty file within a specified subfolder under BASE_DIR."""
    folder_path = make_folder(folder_name)
    file_path = os.path.join(BASE_DIR, folder_name, file_name)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")
    return f"File created successfully at: {file_path}"


@mcp.tool()
def write_to_file(file_name: str, text: str) -> str:
    """Write or overwrite text to a file in BASE_DIR."""
    ensure_base_dir()
    file_path = os.path.join(BASE_DIR, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    return f"Successfully wrote {len(text)} characters to {file_name} in {BASE_DIR}."


# Backward compatibility aliases
startAnApp = start_app
makeAFolder = make_folder
makeAFile = make_file
makeAFil = make_file
writeToFile = write_to_file

if __name__ == "__main__":
    mcp.run()
