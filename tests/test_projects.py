from uuid import uuid4, UUID


def create_project(client):
    body = {
        "name": "test project"
    }

    response = client.post("/projects", json=body)

    return response


def test_create_project(client):
    create_response = create_project(client)

    assert create_response.status_code == 201

    created_project = create_response.json()

    UUID(created_project["project_id"])
    assert created_project["name"] == "test project"


def test_try_to_create_project_without_name(client):
    response = client.post("/projects")

    assert response.status_code == 422


def test_get_project(client):
    create_response = create_project(client)

    project_id = create_response.json()["project_id"]

    get_response = client.get(f"/projects/{project_id}")

    assert get_response.status_code == 200
    assert get_response.json() == create_response.json()


def test_get_project_with_invalid_uuid(client):
    response = client.get("/projects/123")

    assert response.status_code == 422


def test_get_unknown_project(client):
    project_id = uuid4()

    response = client.get(f"/projects/{project_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"