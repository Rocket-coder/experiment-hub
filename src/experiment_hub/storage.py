from pathlib import Path
import sqlite3
import json
from uuid import UUID
from datetime import datetime

from experiment_hub.models import Run, Project, Experiment


DB_PATH = Path("database/runs.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with get_connection() as connection:
        # Table runs init
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            experiment_id TEXT NOT NULL
            status TEXT NOT NULL,
            start_time TEXT NOT NULL,
            program TEXT NOT NULL,
            parameters TEXT NOT NULL,
            results TEXT,
            end_time TEXT
            FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id)
            )
            """
        )

        # Table projects init
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
            project_id TEXT PRIMARY KEY,
            name TEXT NOT NULL
            )
            """
        )

        # Table experiments init
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS experiments (
                experiment_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(project_id)
            )
            """
        )       


def save_project(project: Project):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO projects (
                project_id,
                name
            )
            VALUES (?, ?)
            """,
            (
                str(project.project_id),
                project.name
            )
        )


def get_project(project_id: UUID) -> Project | None:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                project_id,
                name
            FROM projects
            WHERE project_id = ?
            """,
            (str(project_id),)
        )

        row = cursor.fetchone()

    if row is None:
        return None

    return Project(
        project_id=UUID(row[0]),
        name=row[1]
    )


def save_experiment(experiment: Experiment):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO experiments (
                experiment_id,
                project_id,
                name
            )
            VALUES (?, ?, ?)
            """,
            (
                str(experiment.experiment_id),
                str(experiment.project_id),
                experiment.name
            )
        )


def get_experiment(experiment_id: UUID) -> Experiment | None:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                experiment_id,
                project_id,
                name
            FROM experiments
            WHERE experiment_id = ?
            """,
            (str(experiment_id),)
        )

        row = cursor.fetchone()

    if row is None:
        return None

    return Experiment(
        experiment_id=UUID(row[0]),
        project_id=UUID(row[1]),
        name=row[2]
    )


def save_run(run: Run):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO runs (
                run_id,
                experiment_id,
                status,
                start_time,
                program,
                parameters,
                results,
                end_time
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(run.run_id),
                str(run.experiment_id),
                run.status,
                run.start_time.isoformat(),
                run.program,
                json.dumps(run.parameters),
                run.results,
                run.end_time.isoformat() if run.end_time else None
            )
        )


def get_run(run_id: UUID) -> Run | None:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                run_id,
                experiment_id,
                status,
                start_time,
                program,
                parameters,
                results,
                end_time
            FROM runs
            WHERE run_id = ?
            """,
            (str(run_id),)
        )

        row = cursor.fetchone()

    if row is None:
        return None

    return Run(
        run_id=UUID(row[0]),
        experiment_id=UUID(row[1]),
        status=row[2],
        start_time=datetime.fromisoformat(row[3]),
        program=row[4],
        parameters=json.loads(row[5]),
        results=row[6],
        end_time=datetime.fromisoformat(row[7]) if row[7] else None
    )


def get_runs() -> list[Run]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                run_id,
                experiment_id,
                status,
                start_time,
                program,
                parameters,
                results,
                end_time
            FROM runs
            """
        )
    
        all_runs = cursor.fetchall()

    runs = []

    for run in all_runs:
        runs.append(
            Run(
                run_id=UUID(run[0]),
                experiment_id=UUID(run[1]),
                status=run[2],
                start_time=datetime.fromisoformat(run[3]),
                program=run[4],
                parameters=json.loads(run[5]),
                results=run[6],
                end_time=datetime.fromisoformat(run[7]) if run[7] else None
            )
        )

    return runs


def update_run_record(run: Run):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE runs
            SET
                status = ?,
                results = ?,
                end_time = ?
            WHERE run_id = ?
            """,
            (
                run.status,
                run.results,
                run.end_time.isoformat() if run.end_time else None,
                str(run.run_id)
            )
        )