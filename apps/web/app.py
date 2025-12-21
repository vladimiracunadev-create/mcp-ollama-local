import asyncio
from pathlib import Path

import sqlite3
import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from host.settings import load_settings
from host.chat_engine import run_chat
from host.mcp_bridge import open_mcp_session

# -----------------------
# App + paths
# -----------------------
app = FastAPI()

BASE = Path(__file__).resolve().parent
TEMPL = BASE / "templates"
STATIC = BASE / "static"

# Static (no molesta aunque ahora uses JS inline)
if STATIC.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")


# -----------------------
# Models
# -----------------------
class ChatIn(BaseModel):
    message: str


class MCPIn(BaseModel):
    tool: str
    args: dict = {}


# -----------------------
# Helpers
# -----------------------
def _content_to_plain(content):
    out = []
    if not content:
        return out
    for c in content:
        if hasattr(c, "text") and c.text is not None:
            out.append(c.text)
        else:
            out.append(str(c))
    return out


# -----------------------
# Pages
# -----------------------
@app.get("/", response_class=HTMLResponse)
def index():
    return (TEMPL / "index.html").read_text(encoding="utf-8")


@app.get("/chat", response_class=HTMLResponse)
def chat_page():
    return (TEMPL / "chat.html").read_text(encoding="utf-8")


@app.get("/options", response_class=HTMLResponse)
def options_page():
    return (TEMPL / "options.html").read_text(encoding="utf-8")


# -----------------------
# API
# -----------------------
@app.post("/api/chat")
def api_chat(inp: ChatIn):
    s = load_settings()
    try:
        answer = asyncio.run(run_chat(inp.message, s, use_history=True))
        return JSONResponse({"ok": True, "answer": answer})
    except Exception as e:
        # ✅ en vez de 500 ciego, devuelve el error al frontend
        return JSONResponse({"ok": False, "error": str(e)})


@app.post("/api/mcp")
def api_mcp(inp: MCPIn):
    async def _run():
        stack, session = await open_mcp_session()
        try:
            result = await session.call_tool(inp.tool, inp.args)
            return {"ok": True, "tool": inp.tool, "result": _content_to_plain(result.content)}
        finally:
            await stack.aclose()

    try:
        return JSONResponse(asyncio.run(_run()))
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})


@app.get("/api/health")
async def api_health():
    """
    Salud del sistema:
    - web_ok: este server
    - ollama_ok: API de Ollama accesible
    - mcp_ok: tools MCP accesibles (system_info)
    """
    s = load_settings()
    web_ok = True

    # Ollama
    ollama_ok = False
    ollama_detail = ""
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            r = await client.get(f"{s.ollama_url}/api/tags")
            ollama_ok = (r.status_code == 200)
            ollama_detail = "API OK" if ollama_ok else f"HTTP {r.status_code}"
    except Exception as e:
        ollama_ok = False
        ollama_detail = str(e)

    # MCP
    mcp_ok = False
    mcp_detail = ""
    try:
        stack, session = await open_mcp_session()
        try:
            await session.call_tool("system_info", {})
            mcp_ok = True
            mcp_detail = "system_info OK"
        finally:
            await stack.aclose()
    except Exception as e:
        mcp_ok = False
        mcp_detail = str(e)

    return {
        "web_ok": web_ok,
        "ollama_ok": ollama_ok,
        "ollama_detail": ollama_detail,
        "mcp_ok": mcp_ok,
        "mcp_detail": mcp_detail,
    }

@app.get("/history", response_class=HTMLResponse)
def history_page():
    return (TEMPL / "history.html").read_text(encoding="utf-8")


@app.get("/api/history")
def api_history(limit: int = 200, role: str = "", q: str = ""):
    """
    Devuelve historial del chat desde SQLite.
    - limit: cantidad de filas (max recomendado 1000)
    - role: 'user' o 'assistant' (opcional)
    - q: texto a buscar (opcional)
    """
    s = load_settings()

    try:
        con = sqlite3.connect(s.history_db)
        con.row_factory = sqlite3.Row

        # total
        total = con.execute("SELECT COUNT(*) AS c FROM chat").fetchone()["c"]

        where = []
        params = []

        if role:
            where.append("role = ?")
            params.append(role)

        if q:
            where.append("content LIKE ?")
            params.append(f"%{q}%")

        where_sql = ("WHERE " + " AND ".join(where)) if where else ""

        limit = max(10, min(int(limit), 1000))

        rows = con.execute(
            f"SELECT id, ts, role, content FROM chat {where_sql} ORDER BY id DESC LIMIT ?",
            (*params, limit)
        ).fetchall()

        con.close()

        # los devolvemos en orden cronológico (más antiguo -> más nuevo)
        items = [{
            "id": r["id"],
            "ts": r["ts"],
            "role": r["role"],
            "content": r["content"],
        } for r in reversed(rows)]

        return {"ok": True, "total": total, "items": items}

    except Exception as e:
        return {"ok": False, "error": str(e)}

