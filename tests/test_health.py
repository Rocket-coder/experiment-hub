from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    responce = client.get("/health")
    assert responce.status_code == 200
    assert responce.json() == {"status": "ok"}