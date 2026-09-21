from fastapi import FastAPI, HTTPException
from uuid import uuid4, UUID
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from experiment_hub.models import Run, RunCreate, RunUpdate
from experiment_hub.storage import (
    save_run, 
    get_run as storage_get_run, 
    get_runs as storage_get_runs,
    init_db
)
from experiment_hub.service import update_run, RunNotFoundError, RunAlreadyFinishedError


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/runs")
async def get_runs():
    return storage_get_runs()


@app.post("/runs", status_code=201)
async def create_run(run_create: RunCreate):
    run = Run(
        run_id = uuid4(),
        status = "running",
        start_time = datetime.now(timezone.utc),
        program = run_create.program,
        parameters = run_create.parameters
    )

    save_run(run)
    
    return storage_get_run(run.run_id)


@app.get("/runs/{run_id}")
async def get_run(run_id: UUID):
    run = storage_get_run(run_id)
    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Run not found"
        )

    return run


@app.patch("/runs/{run_id}")
async def patch_run(run_id: UUID, run_update: RunUpdate):
    try:
        return update_run(run_id, run_update)
    except RunNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Run not found"
        )
    except RunAlreadyFinishedError:
        raise HTTPException(
            status_code=409,
            detail="Run is already finished"
        )