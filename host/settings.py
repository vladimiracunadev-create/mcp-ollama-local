from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os

@dataclass(frozen=True)
class Settings:
    base_dir: Path
    ollama_url: str
    model: str
    history_db: Path

def load_settings() -> Settings:
    base = Path(__file__).resolve().parents[1]
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    model = os.getenv("MODEL", "qwen3:8b")
    history_db = base / "data" / "chat_history.sqlite"
    return Settings(base, ollama_url, model, history_db)
