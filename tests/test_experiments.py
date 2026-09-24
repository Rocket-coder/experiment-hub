from uuid import UUID, uuid4


def create_experiment(client, api_project):
    experiment_body = {
        "name": "experiment test"
    }

    project_id = api_project["project_id"]

    experiment_create_response = client.post(f"/projects/{project_id}/experiments", json=experiment_body)

    return experiment_create_response


def test_create_experiment(client, api_experiment):
    created_experiment = api_experiment

    UUID(created_experiment["experiment_id"])
    UUID(created_experiment["project_id"])
    assert created_experiment["name"] == "Test experiment"


def test_try_to_create_experiment_without_name(client, api_project):
    project_id = api_project["project_id"]

    create_experiment_repsonse = client.post(f"/projects/{project_id}/experiments")

    assert create_experiment_repsonse.status_code == 422


def test_create_experiment_with_unknown_project(client):
    response = client.post(f"/projects/{uuid4()}/experiments", json={"name": "no project"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_get_experiment(client, api_experiment):
    experiment_id = api_experiment["experiment_id"]

    get_response = client.get(f"/experiments/{experiment_id}")

    assert get_response.status_code == 200
    assert get_response.json() == api_experiment


def test_try_to_get_experiment_with_unknown_uuid(client):
    get_response = client.get(f"/experiments/{uuid4()}")

    assert get_response.status_code == 404


def test_try_to_get_experiment_with_invalid_uuid(client):
    get_response = client.get("/experiments/321")

    assert get_response.status_code == 422