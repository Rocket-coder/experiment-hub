import sqlite3
import pytest
from uuid import uuid4
from datetime import datetime, timezone

from experiment_hub import storage
from experiment_hub.models import Run, Experiment, Project

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


def test_get_unknown_run():
    assert storage.get_run(uuid4()) is None


def test_create_project():
    project = Project(
        project_id=uuid4(),
        name="Test New Project"
    )

    storage.save_project(project)

    db_project = storage.get_project(project.project_id)

    assert project == db_project


def test_save_experiment():
    project = Project(
        project_id=uuid4(),
        name="Project for Experiment"
    )

    storage.save_project(project)

    experiment = Experiment(
        experiment_id=uuid4(),
        project_id=project.project_id,
        name="New Exp"
    )

    storage.save_experiment(experiment)

    db_experiment = storage.get_experiment(experiment.experiment_id)

    assert experiment == db_experiment


def test_get_unknown_project():
    assert storage.get_project(uuid4()) is None


def test_get_unknown_experiment():
    assert storage.get_experiment(uuid4()) is None


def test_cannot_save_experiment_without_project():
    experiment = Experiment(
        experiment_id=uuid4(),
        project_id=uuid4(),
        name="Test Experiment"
    )

    with pytest.raises(sqlite3.IntegrityError):
        storage.save_experiment(experiment)