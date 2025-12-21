from __future__ import annotations
from contextlib import AsyncExitStack
from pathlib import Path
import sys
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

BASE = Path(__file__).resolve().parents[1]
MCP_SERVER_PY = (BASE / "mcp_server" / "server.py").resolve()

async def open_mcp_session() -> tuple[AsyncExitStack, ClientSession]:
    stack = AsyncExitStack()

    # ✅ Usa el python del proceso actual (tu venv)
    cmd = sys.executable
    # ✅ Usa ruta absoluta al server MCP
    args = [str(MCP_SERVER_PY)]

    env = dict(os.environ)
    env["PYTHONUNBUFFERED"] = "1"

    params = StdioServerParameters(command=cmd, args=args, env=env)

    transport = await stack.enter_async_context(stdio_client(params))
    stdio, write = transport
    session = await stack.enter_async_context(ClientSession(stdio, write))
    await session.initialize()
    return stack, session

def mcp_tools_to_ollama(tools) -> list:
    return [{
        "type": "function",
        "function": {
            "name": t.name,
            "description": t.description or "",
            "parameters": t.inputSchema,
        }
    } for t in tools]
