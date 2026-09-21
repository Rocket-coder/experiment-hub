import pytest
from fastapi.testclient import TestClient
from experiment_hub.main import app, runs
from uuid import uuid4, UUID

@pytest.fixture(autouse=True)
def clear_runs():
    runs.clear()
    yield
    runs.clear()


client = TestClient(app)


def create_run():
    body = {
            "program": "test_post.py",
            "parameters": {
                "learning_rate": 0.21,
                "batch_size": 64
            }
        }

    response = client.post("/runs", json=body)

    return response


def test_create_run():
    create_response = create_run()

    assert create_response.status_code == 201

    created_run = create_response.json()

    UUID(created_run["run_id"])    
    assert created_run["status"] == "running"
    assert created_run["program"] == "test_post.py"
    assert created_run["parameters"] == {
        "learning_rate": 0.21,
        "batch_size": 64
    }
    assert created_run["start_time"] is not None
    assert created_run["results"] is None
    assert created_run["end_time"] is None


def test_create_run_without_parameters():
    bad_body = {
        "program": "no_params.py"
    }

    response = client.post("/runs", json=bad_body)

    assert response.status_code == 422


def test_get_run():
    create_response = create_run()

    run_id = create_response.json()["run_id"]
    
    get_response = client.get(f"/runs/{run_id}")

    assert get_response.status_code == 200
    assert get_response.json() == create_response.json()


def test_get_run_with_invalid_uuid():
    response = client.get("/runs/123")

    assert response.status_code == 422


def test_get_unknown_run():
    run_id = uuid4()

    response = client.get(f"/runs/{run_id}")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Run not found"


def test_complete_run():
    create_response = create_run()

    update_body = {
        "status": "completed",
        "results": "test result"
    }

    run_id = create_response.json()["run_id"]
    patch_response = client.patch(f"/runs/{run_id}", json=update_body)

    assert patch_response.status_code == 200

    patch_result = patch_response.json()

    assert patch_result["status"] == "completed"
    assert patch_result["results"] == "test result"
    assert patch_result["end_time"] is not None


def test_fail_run():
    create_response = create_run()

    failed_body = {
        "status": "failed",
        "results": "bad request"
    }

    run_id = create_response.json()["run_id"]
    patch_response = client.patch(f"/runs/{run_id}", json=failed_body)

    assert patch_response.status_code == 200

    patch_result = patch_response.json()
    
    assert patch_result["status"] == "failed"
    assert patch_result["results"] == "bad request"
    assert patch_result["end_time"] is not None


def test_patch_run_with_invalid_status():
    create_response = create_run()

    update_body = {
        "status": "unknown",
        "results": ""
    }

    run_id = create_response.json()["run_id"]
    patch_response = client.patch(f"/runs/{run_id}", json=update_body)

    assert patch_response.status_code == 422


def test_patch_unknown_run():
    update_body = {
            "status": "completed",
            "results": "test result"
        }

    run_id = uuid4()

    patch_response = client.patch(f"/runs/{run_id}", json=update_body)

    assert patch_response.status_code == 404


def test_patch_finished_run():
    create_response = create_run()

    update_body = {
                "status": "completed",
                "results": "test result"
            }

    run_id = create_response.json()["run_id"]

    client.patch(f"/runs/{run_id}", json=update_body)
    update_body = {
                    "status": "failed",
                    "results": "test result"
                }
    another_patch_response = client.patch(f"/runs/{run_id}", json=update_body)

    assert another_patch_response.status_code == 409
    assert another_patch_response.json()["detail"] == "Run is already finished"