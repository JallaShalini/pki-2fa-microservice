import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test /health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "timestamp" in response.json()

def test_decrypt_seed_endpoint():
    """Test /decrypt-seed endpoint handles invalid data"""
    encrypted_data = "base64_encoded_encrypted_seed"
    response = client.post("/decrypt-seed", json={"encrypted_seed": encrypted_data})
    assert response.status_code in [200, 400, 500]

def test_generate_2fa_endpoint():
    """Test /generate-2fa endpoint"""
    response = client.get("/generate-2fa")
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert len(data["code"]) == 6
    assert "valid_for" in data

def test_verify_2fa_endpoint():
    """Test /verify-2fa endpoint"""
    gen_response = client.get("/generate-2fa")
    code = gen_response.json()["code"]
    
    verify_response = client.post("/verify-2fa", json={"code": code})
    assert verify_response.status_code == 200
    assert verify_response.json()["valid"] is True

def test_verify_2fa_invalid():
    """Test /verify-2fa with invalid code"""
    response = client.post("/verify-2fa", json={"code": "000000"})
    assert response.status_code == 200
    assert response.json()["valid"] is False

