from unittest.mock import patch

from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_workflow_endpoint_returns_trace_metadata():
    fake_result = {
        "decision": "Proceed with further evaluation.",
        "errors": [],
        "run_id": "run-123",
        "stage_timings_ms": {"planning": 1.2, "total": 4.5},
    }

    with patch("src.api.main.workflow.run", return_value=fake_result):
        response = client.post(
            "/workflow",
            json={
                "session_id": "session-1",
                "message": "Should we expand?",
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "decision": "Proceed with further evaluation.",
        "errors": [],
        "run_id": "run-123",
        "stage_timings_ms": {"planning": 1.2, "total": 4.5},
    }


def test_workflow_endpoint_rejects_empty_message():
    response = client.post(
        "/workflow",
        json={"session_id": "session-1", "message": ""},
    )

    assert response.status_code == 422
