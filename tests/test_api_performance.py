from time import perf_counter

from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_health_endpoint_handles_repeated_requests_quickly():
    started_at = perf_counter()

    responses = [client.get("/health") for _ in range(20)]

    elapsed_seconds = perf_counter() - started_at

    assert all(response.status_code == 200 for response in responses)
    assert elapsed_seconds < 5


def test_metrics_endpoint_reports_request_activity():
    response = client.get("/metrics")

    assert response.status_code == 200
    payload = response.json()
    assert payload["requests_total"] >= 1
    assert payload["requests_successful"] >= 1
    assert payload["average_latency_ms"] >= 0
