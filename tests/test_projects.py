from uuid import uuid4, UUID


def test_create_project(api_project):
    created_project = api_project

    UUID(created_project["project_id"])
    assert created_project["name"] == "Test Project"


def test_try_to_create_project_without_name(client):
    response = client.post("/projects")

    assert response.status_code == 422


def test_get_project(client, api_project):
    project_id = api_project["project_id"]
    get_response = client.get(f"/projects/{project_id}")

    assert get_response.status_code == 200
    assert get_response.json() == api_project


def test_get_project_with_invalid_uuid(client):
    response = client.get("/projects/123")

    assert response.status_code == 422


def test_get_unknown_project(client):
    project_id = uuid4()

    response = client.get(f"/projects/{project_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"