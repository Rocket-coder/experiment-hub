from pathlib import Path
import sqlite3
import json
from uuid import UUID
from datetime import datetime

from experiment_hub.models import Run


DB_PATH = Path("database/runs.db")


# Создание таблицы runs
def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute('''
        CREATE TABLE IF NOT EXISTS runs (
        run_id TEXT PRIMARY KEY,
        status TEXT NOT NULL,
        start_time TEXT NOT NULL,
        program TEXT NOT NULL,
        parameters TEXT NOT NULL,
        results TEXT,
        end_time TEXT
        )
        ''')


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
                run.end_time.isoformat(),
                str(run.run_id)
            )
        )