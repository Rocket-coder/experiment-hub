from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str


class Project(BaseModel):
    project_id: UUID
    name: str


class ExperimentCreate(BaseModel):
    project_id: UUID
    name: str


class Experiment(BaseModel):
    experiment_id: UUID
    project_id: UUID
    name: str


class RunCreate(BaseModel):
    program: str
    parameters: dict[str, int | float]


class Run(BaseModel):
    run_id: UUID
    status: Literal["running", "completed", "failed", "cancelled"]
    start_time: datetime
    program: str
    parameters: dict[str, int | float]
    results: str | None = None
    end_time: datetime | None = None


class RunUpdate(BaseModel):
    status: Literal["completed", "failed", "cancelled"]
    results: str | None = None