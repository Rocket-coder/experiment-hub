import pytest

from uuid import uuid4
from datetime import datetime, timezone

from experiment_hub import storage
from experiment_hub.models import Run, RunUpdate, Experiment, Project
from experiment_hub.service import update_run, create_experiment, RunAlreadyFinishedError, ProjectNotFoundError


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


def test_create_experiment_with_real_project():
    project = Project(
        project_id=uuid4(),
        name="test project"
    )

    storage.save_project(project)

    experiment = Experiment(
        experiment_id=uuid4(),
        project_id=project.project_id,
        name="test experiment"
    )

    saved_experiment = create_experiment(experiment)

    assert saved_experiment.experiment_id == experiment.experiment_id
    assert saved_experiment.project_id == experiment.project_id
    assert saved_experiment.name == experiment.name


def test_try_to_create_experiment_with_unknown_project():
    experiment = Experiment(
        experiment_id=uuid4(),
        project_id=uuid4(),
        name="bad test experiment"
    )

    with pytest.raises(ProjectNotFoundError):
        create_experiment(experiment)