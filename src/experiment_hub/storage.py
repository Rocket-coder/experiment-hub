from pathlib import Path
import sqlite3
import json
from uuid import UUID
from datetime import datetime

from experiment_hub.models import Run, Project, Experiment


DB_PATH = Path("database/runs.db")


# Создание таблицы runs
def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with sqlite3.connect(DB_PATH) as connection:
        # Table runs init
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            start_time TEXT NOT NULL,
            program TEXT NOT NULL,
            parameters TEXT NOT NULL,
            results TEXT,
            end_time TEXT
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
            project_id TEXT FOREIGN KEY,
            name TEXT NOT NULL
            )
            """
        )       


def save_project(project: Project):
    with sqlite3.connect(DB_PATH) as connection:
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
    with sqlite3.connect(DB_PATH) as connection:
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


def save_experiment(project_id: UUID, experiment: Experiment):
    project = get_project(project_id)

    if project is None:
        # TODO: add error for no project
        raise


    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO experiments (
                experiment_id,
                project_id,
                name
            VALUES (?, ?, ?)
            )
            """,
            (
                str(experiment.experiment_id),
                str(project_id),
                experiment.name
            )
        )


def get_experiment(experiment_id: UUID) -> Experiment | None:
    with sqlite3.connect(DB_PATH) as connection:
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
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO runs (
                run_id,
                status,
                start_time,
                program,
                parameters,
                results,
                end_time
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(run.run_id),
                run.status,
                run.start_time.isoformat(),
                run.program,
                json.dumps(run.parameters),
                run.results,
                run.end_time.isoformat() if run.end_time else None
            )
        )


def get_run(run_id: UUID) -> Run | None:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT
                run_id,
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
        status=row[1],
        start_time=datetime.fromisoformat(row[2]),
        program=row[3],
        parameters=json.loads(row[4]),
        results=row[5],
        end_time=datetime.fromisoformat(row[6]) if row[6] else None
    )


def get_runs() -> list[Run]:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT
                run_id,
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
                status=run[1],
                start_time=datetime.fromisoformat(run[2]),
                program=run[3],
                parameters=json.loads(run[4]),
                results=run[5],
                end_time=datetime.fromisoformat(run[6]) if run[6] else None
            )
        )

    return runs


def update_run_record(run: Run):
    with sqlite3.connect(DB_PATH) as connection:
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