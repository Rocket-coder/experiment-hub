from uuid import UUID
from datetime import datetime, timezone

from experiment_hub.models import Run, RunUpdate
from experiment_hub.storage import runs


class RunNotFoundError(Exception):
    pass


class RunAlreadyFinishedError(Exception):
    pass


def update_run(run_id: UUID, run_update: RunUpdate) -> Run:
    if run_id not in runs:
        raise RunNotFoundError()

    if runs[run_id].status != "running":
        raise RunAlreadyFinishedError()

    runs[run_id].status = run_update.status
    runs[run_id].results = run_update.results
    runs[run_id].end_time = datetime.now(timezone.utc)

    return runs[run_id]