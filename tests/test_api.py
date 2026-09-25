import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set dummy API key for testing if not already set
if not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = "test-key-for-ci"

from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_medicines():
    response = client.get("/api/medicines")
    assert response.status_code == 200
    medicines = response.json()
    assert len(medicines) > 0
    assert medicines[0]["id"]
    assert medicines[0]["name"]

def test_search_medicines():
    response = client.get("/api/medicines/search?q=pantop")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert any("Pantop" in med["name"] for med in results)

def test_search_empty():
    response = client.get("/api/medicines/search?q=nonexistentmedicine123")
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)

@pytest.mark.skipif(
    os.getenv("GEMINI_API_KEY", "").startswith("test-"),
    reason="Chat test skipped in CI without real API key"
)
def test_chat_basic():
    response = client.post("/api/chat", json={"message": "What is Pantop 40?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["answer"], str)
    assert isinstance(data["sources"], list)

def test_root_page():
    response = client.get("/")
    assert response.status_code == 200
