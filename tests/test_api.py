from pathlib import Path

from fastapi.testclient import TestClient

import apps.web.app as web_app
from host.settings import Settings

client = TestClient(web_app.app)


def make_settings(tmp_path: Path, *, api_key=None, require_api_key=False) -> Settings:
    return Settings(
        base_dir=tmp_path,
        ollama_url="http://localhost:11434",
        model="qwen3:8b",
        history_db=tmp_path / "chat_history.sqlite",
        api_key=api_key,
        require_api_key=require_api_key,
        allowed_origins=["http://localhost:8000"],
    )


def test_read_main():
    """Verifica que el home carga."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_health_check_endpoint():
    """Prueba el endpoint de health que usará Kubernetes."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "web_ok" in data
    assert data["web_ok"] is True


def test_history_endpoint():
    """Prueba que el endpoint html de history funciona."""
    response = client.get("/history")
    assert response.status_code == 200


def test_options_endpoint():
    """Prueba que el endpoint de configuraciones frontend responde."""
    response = client.get("/options")
    assert response.status_code == 200


def test_chat_page():
    """Verifica la carga inicial de la página de chat."""
    response = client.get("/chat")
    assert response.status_code == 200


def test_api_history_empty():
    """Prueba que la API de historia retorne estructura JSON sin fallar"""
    response = client.get("/api/history?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "ok" in data


def test_health_allows_anonymous_when_api_key_is_optional(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(
        web_app, "load_settings", lambda: make_settings(tmp_path, api_key="secret")
    )
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["auth_required"] is False


def test_health_requires_api_key_when_enabled(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(
        web_app,
        "load_settings",
        lambda: make_settings(tmp_path, api_key="secret", require_api_key=True),
    )
    forbidden = client.get("/api/health")
    assert forbidden.status_code == 403
    assert forbidden.json()["ok"] is False

    allowed = client.get("/api/health", headers={"X-API-Key": "secret"})
    assert allowed.status_code == 200


def test_chat_rejects_empty_messages():
    response = client.post("/api/chat", json={"message": "   "})
    assert response.status_code == 422
    assert response.json()["ok"] is False


def test_chat_returns_upstream_errors(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(
        web_app, "load_settings", lambda: make_settings(tmp_path, api_key=None)
    )

    async def fake_run_chat(*args, **kwargs):
        raise RuntimeError("upstream down")

    monkeypatch.setattr(web_app, "run_chat", fake_run_chat)
    response = client.post("/api/chat", json={"message": "hola"})
    assert response.status_code == 502
    assert response.json() == {"ok": False, "error": "upstream down"}
