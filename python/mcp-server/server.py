"""Aira MCP Server — expose Aira tools to any MCP-compatible AI assistant.

Usage:
    pip install aira-sdk[mcp]
    export AIRA_API_KEY="aira_live_xxx"
    python server.py
"""

from aira.extras.mcp import create_aira_mcp_server

server = create_aira_mcp_server()

if __name__ == "__main__":
    server.run()
