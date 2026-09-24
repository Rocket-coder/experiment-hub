import json
from uuid import UUID, uuid4


def create_experiment(client):
    project_body = {
        "name": "test project"
    }

    experiment_body = {
        "name": "experiment test"
    }

    project_create_response = client.post("/projects", json=project_body)
    project_id = project_create_response.json()["project_id"]

    experiment_create_response = client.post(f"/projects/{project_id}/experiments", json=experiment_body)

    return experiment_create_response


def test_create_experiment(client):
    create_response = create_experiment(client)

    assert create_response.status_code == 201

    created_experiment = create_response.json()

    UUID(created_experiment["experiment_id"])
    UUID(created_experiment["project_id"])
    assert created_experiment["name"] == "experiment test"


def test_try_to_create_experiment_without_name(client):
    project_body = {
        "name": "Test Project"
    }
    create_project_response = client.post("/projects", json=project_body)

    project_id = create_project_response.json()["project_id"]

    create_experiment_repsonse = client.post(f"/projects/{project_id}/experiments")

    assert create_experiment_repsonse.status_code == 422


def test_create_experiment_with_unknown_project(client):
    body = {
        "name": "no project"
    }

    response = client.post(f"/projects/{uuid4()}/experiments", json=body)

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_get_experiment(client):
    create_response = create_experiment(client)

    experiment_id = create_response.json()["experiment_id"]

    get_response = client.get(f"/experiments/{experiment_id}")

    assert get_response.status_code == 200
    assert get_response.json() == create_response.json()


def test_try_to_get_experiment_with_unknown_uuid(client):
    get_response = client.get(f"/experiments/{uuid4()}")

    assert get_response.status_code == 404


def test_try_to_get_experiment_with_invalid_uuid(client):
    get_response = client.get("/experiments/321")

    assert get_response.status_code == 422