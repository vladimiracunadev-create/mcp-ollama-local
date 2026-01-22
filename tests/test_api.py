from fastapi.testclient import TestClient
from apps.web.app import app

client = TestClient(app)

def test_read_main():
    """Test básico para verificar que la app responde."""
    response = client.get("/")
    # Puede devolver 200 o redireccionar si hay auth, 
    # pero asumiremos por ahora que verifica que no explote (404 o 500)
    assert response.status_code in [200, 307, 308]
