
from fastapi.testclient import TestClient
from tnpo.inference import app

client = TestClient(app)

def test_inference_endpoint():
    payload = {"input": [1, 3, 5]}
    expected_output = [2, 6, 10]

    response = client.post("/infer", json=payload)
    assert response.status_code == 200
    assert response.json().get("output") == expected_output

def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


