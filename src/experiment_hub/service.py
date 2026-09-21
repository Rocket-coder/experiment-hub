from uuid import UUID
from datetime import datetime, timezone

from experiment_hub.models import Run, RunUpdate
from experiment_hub.storage import get_run, update_run_record


class RunNotFoundError(Exception):
    pass


class RunAlreadyFinishedError(Exception):
    pass


def update_run(run_id: UUID, run_update: RunUpdate) -> Run:
    run = get_run(run_id)

    if run is None:
        raise RunNotFoundError()

    if run.status != "running":
        raise RunAlreadyFinishedError()

    run.status = run_update.status
    run.results = run_update.results
    run.end_time = datetime.now(timezone.utc)

    update_run_record(run)

    return run