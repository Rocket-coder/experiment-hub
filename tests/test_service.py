import pytest

from uuid import uuid4
from datetime import datetime, timezone

from experiment_hub import storage
from experiment_hub.models import Run, RunUpdate
from experiment_hub.service import update_run, RunAlreadyFinishedError


@pytest.fixture(autouse=True)
def test_database(tmp_path, monkeypatch):
    test_db_path = tmp_path / "runs.db"

    monkeypatch.setattr(
        storage,
        "DB_PATH",
        test_db_path
    )

    storage.init_db()


def test_update_running_to_completed():
    run = Run(
        run_id = uuid4(),
        status = "running",
        start_time = datetime.now(timezone.utc),
        program = "unit_test.py",
        parameters = {
            "param1": 25,
            "param2": 5.1
        }
    )

    storage.save_run(run)

    update = RunUpdate(
        status="completed",
        results="ok"
    )

    updated_run = update_run(run.run_id, update)

    assert updated_run.status == "completed"
    assert updated_run.results == "ok"
    assert updated_run.end_time is not None


def test_try_to_update_finished_run():
    run = Run(
            run_id = uuid4(),
            status = "running",
            start_time = datetime.now(timezone.utc),
            program = "unit_test.py",
            parameters = {
                "param1": 25,
                "param2": 5.1
            }
        )
    storage.save_run(run)

    update = RunUpdate(
        status="completed",
        results="ok"
    )

    update_run(run.run_id, update)

    update = RunUpdate(
        status="failed",
        results="Bad request"
    )

    with pytest.raises(RunAlreadyFinishedError):
        update_run(run.run_id, update)