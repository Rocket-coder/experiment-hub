from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4, UUID
from datetime import datetime, timezone

class RunCreate(BaseModel):
    program: str
    parameters: dict[str, int | float]

class Run(BaseModel):
    run_id: UUID
    status: str
    start_time: datetime
    program: str
    parameters: dict[str, int | float]
    results: str | None = None
    end_time: datetime | None = None


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

runs: dict[UUID, Run] = {}

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