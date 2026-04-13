import httpx


async def ollama_chat(
    ollama_url: str, model: str, messages: list, tools: list | None = None
):
    payload = {
        "model": model,
        "messages": messages,
        "tools": tools or [],
        "stream": False,
    }

    try:
        timeout = httpx.Timeout(120.0, connect=5.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(f"{ollama_url}/api/chat", json=payload)
            response.raise_for_status()
    except httpx.TimeoutException as exc:
        raise RuntimeError(
            "Ollama did not respond before the configured timeout."
        ) from exc
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        detail = exc.response.text[:200].strip()
        raise RuntimeError(
            f"Ollama returned HTTP {status} for model {model!r}. "
            f"Detail: {detail or 'empty body'}"
        ) from exc
    except httpx.HTTPError as exc:
        raise RuntimeError(f"Could not connect to Ollama at {ollama_url}.") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("Ollama returned a non-JSON response.") from exc

    message = data.get("message")
    if not isinstance(message, dict):
        raise RuntimeError("Ollama response did not include a valid 'message' object.")
    return message
