import asyncio
import sqlite3
import time
from collections import defaultdict
from pathlib import Path

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.api_key import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from host.chat_engine import run_chat
from host.mcp_bridge import open_mcp_session
from host.settings import load_settings

# -----------------------
# Auth & Security
# -----------------------
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    settings = load_settings()
    if not settings.api_key:
        return None
    if api_key_header == settings.api_key:
        return api_key_header
    raise HTTPException(status_code=403, detail="Could not validate credentials")


# -----------------------
# App + paths
# -----------------------
app = FastAPI()
settings = load_settings()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting (Simple in-memory)
RATE_LIMIT_STASH = defaultdict(list)
RATE_LIMIT_MAX = 60  # requests
RATE_LIMIT_WINDOW = 60  # seconds


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()

    RATE_LIMIT_STASH[client_ip] = [
        t for t in RATE_LIMIT_STASH[client_ip] if now - t < RATE_LIMIT_WINDOW
    ]

    if len(RATE_LIMIT_STASH[client_ip]) >= RATE_LIMIT_MAX:
        return JSONResponse(
            status_code=429,
            content={"ok": False, "error": "Rate limit exceeded. Slow down."},
        )

    RATE_LIMIT_STASH[client_ip].append(now)
    return await call_next(request)


# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self' http://localhost:11434 http://127.0.0.1:11434;"
    )
    response.headers["Content-Security-Policy"] = csp
    return response


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
def api_chat(inp: ChatIn, api_key: str = Depends(get_api_key)):
    s = load_settings()
    try:
        answer = asyncio.run(run_chat(inp.message, s, use_history=True))
        return JSONResponse({"ok": True, "answer": answer})
    except Exception as e:
        # ✅ en vez de 500 ciego, devuelve el error al frontend
        return JSONResponse({"ok": False, "error": str(e)})


@app.post("/api/mcp")
def api_mcp(inp: MCPIn, api_key: str = Depends(get_api_key)):
    async def _run():
        stack, session = await open_mcp_session()
        try:
            result = await session.call_tool(inp.tool, inp.args)
            return {
                "ok": True,
                "tool": inp.tool,
                "result": _content_to_plain(result.content),
            }
        finally:
            await stack.aclose()

    try:
        return JSONResponse(asyncio.run(_run()))
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})


@app.get("/api/health")
async def api_health(api_key: str = Depends(get_api_key)):
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
            ollama_ok = r.status_code == 200
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
def api_history(
    limit: int = 200, role: str = "", q: str = "", api_key: str = Depends(get_api_key)
):
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

        limit = max(10, min(int(limit), 1000))

        query_parts = ["SELECT id, ts, role, content FROM chat"]
        if where:
            query_parts.append("WHERE " + " AND ".join(where))
        query_parts.append("ORDER BY id DESC LIMIT ?")

        query = " ".join(query_parts)

        # Usamos parámetros para evitar SQL Injection (nosec B608)
        rows = con.execute(query, (*params, limit)).fetchall()

        con.close()

        # los devolvemos en orden cronológico (más antiguo -> más nuevo)
        items = [
            {
                "id": r["id"],
                "ts": r["ts"],
                "role": r["role"],
                "content": r["content"],
            }
            for r in reversed(rows)
        ]

        return {"ok": True, "total": total, "items": items}

    except Exception as e:
        return {"ok": False, "error": str(e)}
