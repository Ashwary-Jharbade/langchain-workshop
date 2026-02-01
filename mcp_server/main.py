from mcp.server.fastmcp import FastMCP
from pathlib import Path
from mcp.types import PromptMessage, TextContent

app = FastMCP("local-mcp-server")

@app.tool()
def add(a: int, b: int) -> int:
    """
        Add two integers.
        Accepts:
            a: First integer
            b: Second integer
        Returns:
            The sum of a and b
        Example:
            Prompt: Add 2 and 3
            Response: 5
    """
    return a + b

@app.resource("file://documents/{name}")
def read_document(name: str) -> str:
    """Only read a .txt document by name."""
    # This would normally read from 
    BASE_DIR = Path(__file__).parent
    file_path = BASE_DIR / "documents" / f"{name}"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return f"Content of {name}:\n" + file.read()
    except FileNotFoundError:
        return "Document not found."

# TODO: Need fix
# @app.prompt("hr-policy-summary")
# def hr_policy_summary():
#     """Prompt to summarize HR policy."""
#     return {
#         "messages": [
#             PromptMessage(
#                 role="user",
#                 content=TextContent(
#                     type="text",
#                     text="Summarize this policy."
#                 )
#             )
#         ]
#     }

if __name__ == "__main__":
    app.run(transport="streamable-http")