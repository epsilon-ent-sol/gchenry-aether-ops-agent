"""
Tests SPIFFE interceptor enforcement.
"""
from fastapi.testclient import TestClient
from app.main import app
import jwt

client = TestClient(app)

def test_health_endpoint_public():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_unauthorized_request_rejected():
    res = client.post("/api/v1/agent/invoke", json={"prompt": "Deploy app"})
    assert res.status_code == 401

def test_authorized_spiffe_request():
    token = jwt.encode(
        {"spiffe_id": "spiffe://aether.internal/ns/devops/sa/release-gate", "role": "admin"},
        "secret",
        algorithm="HS256"
    )
    headers = {"Authorization": f"Bearer {token}"}
    res = client.post("/api/v1/agent/invoke", json={"prompt": "Deploy my container"}, headers=headers)
    assert res.status_code == 200
    assert res.json()["actor_spiffe_id"] == "spiffe://aether.internal/ns/devops/sa/release-gate"

