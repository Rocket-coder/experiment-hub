from fastapi import FastAPI, HTTPException
from uuid import uuid4, UUID
from datetime import datetime, timezone

from experiment_hub.models import Run, RunCreate, RunUpdate
from experiment_hub.storage import runs


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/runs")
async def get_runs():
    return list(runs.values())


@app.post("/runs", status_code=201)
async def create_run(run_create: RunCreate):
    run = Run(
        run_id = uuid4(),
        status = "running",
        start_time = datetime.now(timezone.utc),
        program = run_create.program,
        parameters = run_create.parameters
    )

    runs[run.run_id] = run
    
    return run


@app.get("/runs/{run_id}")
async def get_run(run_id: UUID):
    if run_id not in runs:
        raise HTTPException(
            status_code=404,
            detail="Run not found"
        )

    return runs[run_id]


@app.patch("/runs/{run_id}")
async def patch_run(run_id: UUID, run_update: RunUpdate):
    if run_id not in runs:
        raise HTTPException(
            status_code=404,
            detail="Run not found"
        )

    if runs[run_id].status != "running":
        raise HTTPException(
            status_code=409,
            detail="Run is already finished"
        )

    runs[run_id].status = run_update.status
    runs[run_id].results = run_update.results
    runs[run_id].end_time = datetime.now(timezone.utc)

    return runs[run_id]