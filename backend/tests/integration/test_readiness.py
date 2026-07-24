def test_readiness_endpoint(client):
    response = client.get("/ready")

    assert response.status_code == 200

    payload = response.json()
    assert "status" in payload
    assert "dependencies" in payload
    assert "capabilities" in payload
