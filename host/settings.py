from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse


@dataclass(frozen=True)
class Settings:
    base_dir: Path
    ollama_url: str
    model: str
    history_db: Path
    api_key: str | None = None
    require_api_key: bool = False
    allowed_origins: list[str] = field(default_factory=list)


def _parse_bool(name: str, value: str | None, default: bool = False) -> bool:
    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean value, got: {value!r}")


def _parse_origins(raw: str) -> list[str]:
    origins = [item.strip() for item in raw.split(",") if item.strip()]
    return origins or ["http://localhost:8000", "http://127.0.0.1:8000"]


def _validate_http_url(name: str, value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"{name} must be a valid http(s) URL, got: {value!r}")
    return value.rstrip("/")


def load_settings() -> Settings:
    base = Path(__file__).resolve().parents[1]
    data_dir = Path(os.getenv("DATA_DIR", str(base / "data")))

    ollama_url = _validate_http_url(
        "OLLAMA_URL", os.getenv("OLLAMA_URL", "http://localhost:11434")
    )
    model = os.getenv("MODEL", "qwen3:8b").strip()
    api_key = os.getenv("API_KEY")
    require_api_key = _parse_bool(
        "REQUIRE_API_KEY", os.getenv("REQUIRE_API_KEY"), default=False
    )
    allowed_origins = _parse_origins(
        os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000")
    )
    history_db = data_dir / "chat_history.sqlite"

    if not model:
        raise ValueError("MODEL must not be empty.")
    if require_api_key and not api_key:
        raise ValueError(
            "CRITICAL: REQUIRE_API_KEY is true but no API_KEY is set in environment."
        )

    data_dir.mkdir(parents=True, exist_ok=True)

    return Settings(
        base, ollama_url, model, history_db, api_key, require_api_key, allowed_origins
    )
