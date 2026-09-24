import py
import json
import pytest

from fastapi.testclient import TestClient

from uuid import uuid4

from experiment_hub import storage
from experiment_hub.main import app
from experiment_hub.models import Run, Experiment, Project


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def test_database(tmp_path, monkeypatch):
    test_db_path = tmp_path / "runs.db"

    monkeypatch.setattr(
        storage,
        "DB_PATH",
        test_db_path
    )

    storage.init_db()


@pytest.fixture
def project() -> Project:
    project = Project(
        project_id=uuid4(),
        name="XZ name"
    )

    storage.save_project(project)

    return project


@pytest.fixture
def experiment(project) -> Experiment:
    experiment = Experiment(
        experiment_id=uuid4(),
        project_id=project.project_id,
        name="Xz exp"
    )

    storage.save_experiment(experiment)

    return experiment


@pytest.fixture
def api_project(client):
    response = client.post(
        "/projects",
        json={"name": "Test Project"}
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def api_experiment(client, api_project):
    project_id = api_project["project_id"]

    response = client.post(
        f"/projects/{project_id}/experiments",
        json={"name": "Test experiment"}
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def api_run(client, api_experiment):
    body = {
            "program": "test_post.py",
            "parameters": {
                "learning_rate": 0.21,
                "batch_size": 64
            }
        }

    experiment_id = api_experiment["experiment_id"]
    
    response = client.post(f"/experiments/{experiment_id}/runs", json=body)

    assert response.status_code == 201

    return response.json()