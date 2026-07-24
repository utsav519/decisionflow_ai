def test_backend_generates_correlation_id(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers.get("X-Correlation-ID")


def test_backend_preserves_client_correlation_id(client):
    correlation_id = "cor_integration_test_001"

    response = client.get(
        "/health",
        headers={"X-Correlation-ID": correlation_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == correlation_id
