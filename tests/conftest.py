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


def create_test_project() -> Project:
    project = Project(
        project_id=uuid4(),
        name="XZ name"
    )

    storage.save_project(project)

    return project


def create_test_experiment() -> Experiment:
    project_id = create_test_project().project_id

    experiment = Experiment(
        experiment_id=uuid4(),
        project_id=project_id,
        name="Xz exp"
    )

    storage.save_experiment(experiment)

    return experiment