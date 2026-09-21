from uuid import uuid4
from datetime import datetime, timezone

from experiment_hub import storage
from experiment_hub.storage import save_run, get_run
from experiment_hub.models import Run

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

    save_run(run)

    loaded_run = get_run(run.run_id)

    assert loaded_run is not None

    print(loaded_run)