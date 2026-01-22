import json
import sqlite3

from .mcp_bridge import mcp_tools_to_ollama, open_mcp_session
from .ollama_client import ollama_chat


def init_db(db_path):
    con = sqlite3.connect(db_path)
    con.execute("""
      CREATE TABLE IF NOT EXISTS chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts DATETIME DEFAULT CURRENT_TIMESTAMP,
        role TEXT NOT NULL,
        content TEXT NOT NULL
      )
    """)
    con.commit()
    con.close()

def save_msg(db_path, role, content):
    con = sqlite3.connect(db_path)
    con.execute("INSERT INTO chat(role, content) VALUES (?, ?)", (role, content))
    con.commit()
    con.close()

def _tool_content_to_text(content) -> str:
    parts = []
    if not content:
        return ""
    for c in content:
        if hasattr(c, "text") and c.text is not None:
            parts.append(c.text)
        elif isinstance(c, (dict, list)):
            parts.append(json.dumps(c, ensure_ascii=False))
        else:
            parts.append(str(c))
    return "\n".join(parts)

async def run_chat(user_text: str, settings, use_history: bool = True) -> str:
    if use_history:
        init_db(settings.history_db)

    stack, session = await open_mcp_session()
    try:
        tools = (await session.list_tools()).tools
        ollama_tools = mcp_tools_to_ollama(tools)

        system_msg = {
            "role": "system",
            "content": (
                "Responde SIEMPRE en español. "
                "Usa herramientas SOLO si son necesarias para responder."
            )
        }

        messages = [system_msg, {"role": "user", "content": user_text}]

        if use_history:
            save_msg(settings.history_db, "user", user_text)

        # 1) Primera respuesta del modelo
        assistant = await ollama_chat(
            settings.ollama_url, settings.model, messages, ollama_tools
        )
        messages.append(assistant)

        tool_calls = assistant.get("tool_calls") or []

        # ✅ SI NO HAY TOOLS: devolvemos respuesta directa (NO hacemos segunda llamada)
        if not tool_calls:
            out = assistant.get("content") or ""
            if use_history:
                save_msg(settings.history_db, "assistant", out)
            return out

        # 2) Si hay tools, las ejecutamos y hacemos una segunda llamada
        for call in tool_calls:
            fn = (call.get("function") or {}).get("name")
            args_raw = (call.get("function") or {}).get("arguments") or {}

            if isinstance(args_raw, str):
                try:
                    args = json.loads(args_raw)
                except Exception:
                    args = {}
            elif isinstance(args_raw, dict):
                args = args_raw
            else:
                args = {}

            result = await session.call_tool(fn, args)
            tool_text = _tool_content_to_text(result.content)

            messages.append({
                "role": "tool",
                "tool_name": fn,
                "content": tool_text
            })

        final_msg = await ollama_chat(
            settings.ollama_url, settings.model, messages, ollama_tools
        )
        out = final_msg.get("content") or ""

        if use_history:
            save_msg(settings.history_db, "assistant", out)

        return out
    finally:
        await stack.aclose()
