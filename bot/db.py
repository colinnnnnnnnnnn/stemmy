import atexit
import os
from contextlib import contextmanager
from typing import Any, LiteralString

from psycopg import Error as PsycopgError
from psycopg import IntegrityError, OperationalError
from psycopg_pool import ConnectionPool

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://bot:botpass@localhost:5432/jobdb"
)
pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=5)
atexit.register(pool.close)


class DbError(Exception):
    pass


class JobAlreadyExistsError(DbError):
    pass


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


"""
Primitive functions
"""


@contextmanager
def get_conn():
    with pool.connection() as conn:
        yield conn


def fetch_one(query: LiteralString, params: tuple = ()):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchone()


def fetch_all(query: LiteralString, params: tuple = ()):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()


def execute(query: LiteralString, params: tuple = ()):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()
