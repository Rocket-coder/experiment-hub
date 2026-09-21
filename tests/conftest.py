import pytest

from experiment_hub import storage

@pytest.fixture(autouse=True)
def test_database(tmp_path, monkeypatch):
    test_db_path = tmp_path / "runs.db"

    monkeypatch.setattr(
        storage,
        "DB_PATH",
        test_db_path
    )

    storage.init_db()