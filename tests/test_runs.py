from uuid import uuid4, UUID


def test_create_run(api_run):
    created_run = api_run

    UUID(created_run["run_id"])
    UUID(created_run["experiment_id"])    
    assert created_run["status"] == "running"
    assert created_run["program"] == "test_post.py"
    assert created_run["parameters"] == {
        "learning_rate": 0.21,
        "batch_size": 64
    }
    assert created_run["start_time"] is not None
    assert created_run["results"] is None
    assert created_run["end_time"] is None


def test_create_run_without_parameters(client, api_experiment):
    bad_body = {
        "program": "no_params.py"
    }

    experiment_id = api_experiment["experiment_id"]

    response = client.post(f"/experiments/{experiment_id}/runs", json=bad_body)

    assert response.status_code == 422


def test_create_run_with_unknown_experiment(client):
    body = {
        "program": "params?",
        "parameters": {
            "param1": 2.5
        }
    }

    response = client.post(f"/experiments/{uuid4()}/runs", json=body)

    assert response.status_code == 404
    assert response.json()["detail"] == "Experiment not found"


def test_get_run(client, api_run):
    run_id = api_run["run_id"]
    
    get_response = client.get(f"/runs/{run_id}")

    assert get_response.status_code == 200
    assert get_response.json() == api_run


def test_get_run_with_invalid_uuid(client):
    response = client.get("/runs/123")

    assert response.status_code == 422


def test_get_unknown_run(client):
    run_id = uuid4()

    response = client.get(f"/runs/{run_id}")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Run not found"


def test_complete_run(client, api_run):
    update_body = {
        "status": "completed",
        "results": "test result"
    }

    run_id = api_run["run_id"]
    patch_response = client.patch(f"/runs/{run_id}", json=update_body)

    assert patch_response.status_code == 200

    patch_result = patch_response.json()

    assert patch_result["status"] == "completed"
    assert patch_result["results"] == "test result"
    assert patch_result["end_time"] is not None


def test_fail_run(client, api_run):

    failed_body = {
        "status": "failed",
        "results": "bad request"
    }

    run_id = api_run["run_id"]
    patch_response = client.patch(f"/runs/{run_id}", json=failed_body)

    assert patch_response.status_code == 200

    patch_result = patch_response.json()
    
    assert patch_result["status"] == "failed"
    assert patch_result["results"] == "bad request"
    assert patch_result["end_time"] is not None


def test_patch_run_with_invalid_status(client, api_run):
    update_body = {
        "status": "unknown",
        "results": ""
    }

    run_id = api_run["run_id"]
    patch_response = client.patch(f"/runs/{run_id}", json=update_body)

    assert patch_response.status_code == 422


def test_patch_unknown_run(client):
    update_body = {
            "status": "completed",
            "results": "test result"
        }

    run_id = uuid4()

    patch_response = client.patch(f"/runs/{run_id}", json=update_body)

    assert patch_response.status_code == 404


def test_patch_finished_run(client, api_run):
    update_body = {
                "status": "completed",
                "results": "test result"
            }

    run_id = api_run["run_id"]

    client.patch(f"/runs/{run_id}", json=update_body)
    update_body = {
                    "status": "failed",
                    "results": "test result"
                }
    another_patch_response = client.patch(f"/runs/{run_id}", json=update_body)

    assert another_patch_response.status_code == 409
    assert another_patch_response.json()["detail"] == "Run is already finished"


def test_get_runs_empty(client):
    get_response = client.get("/runs")

    assert get_response.status_code == 200
    assert get_response.json() == []


def test_get_runs(client, api_run):
    get_response = client.get("/runs")

    assert get_response.status_code == 200
    assert len(get_response.json()) == 1