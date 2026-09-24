import sqlite3
import pytest
from uuid import uuid4
from datetime import datetime, timezone

from experiment_hub import storage
from experiment_hub.models import Run, Experiment

def test_init_and_save_runs_with_get():
    run = Run(
        run_id=uuid4(),
        status="running",
        start_time=datetime.now(timezone.utc),
        program="test_db.py",
        parameters={
            "test1": 1,
            "test2": 2.5
        }
    )

    storage.save_run(run)

    loaded_run = storage.get_run(run.run_id)

    assert loaded_run == run

    print(loaded_run)


def test_cannot_save_experiment_without_project():
    experiment = Experiment(
        experiment_id=uuid4(),
        project_id=uuid4(),
        name="Test Experiment"
    )

    with pytest.raises(sqlite3.IntegrityError):
        storage.save_experiment(experiment)