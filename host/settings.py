from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    base_dir: Path
    ollama_url: str
    model: str
    history_db: Path
    api_key: str | None = None
    require_api_key: bool = False
    allowed_origins: list[str] = ("*",)


def load_settings() -> Settings:
    base = Path(__file__).resolve().parents[1]
    # Permitir sobreescribir el directorio de datos (útil para Docker/K8s)
    data_dir = Path(os.getenv("DATA_DIR", str(base / "data")))

    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    model = os.getenv("MODEL", "qwen3:8b")
    api_key = os.getenv("API_KEY")
    require_api_key = os.getenv("REQUIRE_API_KEY", "false").lower() == "true"
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")
    history_db = data_dir / "chat_history.sqlite"

    if require_api_key and not api_key:
        raise ValueError(
            "CRITICAL: REQUIRE_API_KEY is true but no API_KEY is set in environment."
        )

    # Asegurar que el directorio de datos exista
    data_dir.mkdir(parents=True, exist_ok=True)

    return Settings(
        base, ollama_url, model, history_db, api_key, require_api_key, allowed_origins
    )
