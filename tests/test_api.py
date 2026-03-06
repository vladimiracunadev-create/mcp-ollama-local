from fastapi.testclient import TestClient

from apps.web.app import app

client = TestClient(app)


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
