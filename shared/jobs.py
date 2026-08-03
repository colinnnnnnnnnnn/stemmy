import uuid
from typing import Any, LiteralString, cast

from psycopg import Error as PsycopgError
from psycopg import IntegrityError, OperationalError

from shared.db import execute, fetch_one, pool
from shared.exceptions import (
    DbError,
    InvalidJobUpdateError,
    JobAlreadyExistsError,
    JobNotFoundError,
)

UPDATABLE_FIELDS = {
    "status",
    "progress",
    "input_path",
    "output_path",
    "error",
    "song_title",
}


def update_job(job_id: str, **fields: Any) -> None:
    invalid = set(fields) - UPDATABLE_FIELDS
    if invalid:
        raise InvalidJobUpdateError(f"Cannot update unknown job fields: {invalid}")

    set_clause = ", ".join(f"{field} = %s" for field in fields)
    query = cast(
        LiteralString,
        f"""
        UPDATE jobs
        SET {set_clause}, updated_at = now()
        WHERE id = %s
        """,
    )
    params = (*fields.values(), job_id)

    try:
        rowcount = execute(query, params)
    except OperationalError as e:
        raise DbError("Database is unavailable") from e
    except PsycopgError as e:
        raise DbError(f"Failed to update job {job_id}") from e

    if rowcount == 0:
        raise JobNotFoundError(f"Job {job_id} not found")


def insert_job(
    job_id: str, telegram_chat_id: int, youtube_url: str, status: str = "queued"
) -> None:
    try:
        execute(
            """
            INSERT INTO jobs (id, telegram_chat_id, youtube_url, status)
            VALUES (%s, %s, %s, %s)
            """,
            (job_id, telegram_chat_id, youtube_url, status),
        )
    except IntegrityError as e:
        raise JobAlreadyExistsError(f"Job {job_id} already exists") from e
    except OperationalError as e:
        raise DbError("Database is unavailable") from e
    except PsycopgError as e:
        raise DbError("Failed to insert job") from e


def fetch_last_job() -> tuple[Any, ...] | None:
    try:
        return fetch_one(
            """
            SELECT id, telegram_chat_id, youtube_url, status, created_at
            FROM jobs
            ORDER BY created_at DESC, id DESC
            LIMIT 1
            """
        )
    except OperationalError as e:
        raise DbError("Database is unavailable") from e
    except PsycopgError as e:
        raise DbError("Failed to fetch last job") from e


def create_job_from_url(telegram_chat_id: int, url: str) -> str:
    job_id = uuid.uuid4().hex
    insert_job(job_id, telegram_chat_id, url)
    return job_id


def mark_job_downloading(job_id: str) -> None:
    update_job(job_id, status="downloading")


def mark_job_failed(job_id: str, error: str) -> None:
    update_job(job_id, status="failed", error=error)


def mark_job_queued(job_id: str, input_path: str) -> None:
    update_job(job_id, status="queued", input_path=input_path)


def update_job_song_title(job_id: str, song_title: str) -> None:
    update_job(job_id, song_title=song_title)


if __name__ == "__main__":
    try:
        url = "https://www.youtube.com/watch?v=qlhahaRSBzw"
        create_job_from_url(123456789, url)
        print(fetch_last_job())
    finally:
        pool.close()
