import httpx


async def ollama_chat(
    ollama_url: str, model: str, messages: list, tools: list | None = None
):
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{ollama_url}/api/chat", json={
            "model": model,
            "messages": messages,
            "tools": tools or [],
            "stream": False
        })
        r.raise_for_status()
        return r.json()["message"]
