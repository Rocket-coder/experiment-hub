import pytest

from fastapi.testclient import TestClient

from experiment_hub import storage
from experiment_hub.main import app


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