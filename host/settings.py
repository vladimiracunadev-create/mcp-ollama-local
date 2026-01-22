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


def load_settings() -> Settings:
    base = Path(__file__).resolve().parents[1]
    # Permitir sobreescribir el directorio de datos (útil para Docker/K8s)
    data_dir = Path(os.getenv("DATA_DIR", str(base / "data")))

    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    model = os.getenv("MODEL", "qwen3:8b")
    history_db = data_dir / "chat_history.sqlite"

    # Asegurar que el directorio de datos exista
    data_dir.mkdir(parents=True, exist_ok=True)

    return Settings(base, ollama_url, model, history_db)
