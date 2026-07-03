import os
from contextlib import contextmanager
from typing import LiteralString

from psycopg_pool import ConnectionPool

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://bot:botpass@localhost:5432/jobdb"
)
pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=5)


def insert_job(
    job_id: str, telegram_chat_id: int, youtube_url: str, status: str = "queued"
) -> None:
    execute(
        """
        INSERT INTO jobs (id, telegram_chat_id, youtube_url, status)
        VALUES (%s, %s, %s, %s)
        """,
        (job_id, telegram_chat_id, youtube_url, status),
    )


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
