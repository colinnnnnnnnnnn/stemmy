import atexit
import os
from contextlib import contextmanager
from typing import Any, LiteralString

from psycopg import Error as PsycopgError
from psycopg import IntegrityError, OperationalError
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://bot:botpass@localhost:5432/jobdb"
)
pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=5)
atexit.register(pool.close)


"""
Primitive functions
"""


@contextmanager
def get_conn():
    with pool.connection() as conn:
        yield conn


def fetch_one(query: LiteralString, params: tuple = ()) -> dict[str, Any] | None:
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, params)
        return cur.fetchone()


def fetch_all(query: LiteralString, params: tuple = ()) -> list[dict[str, Any]]:
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, params)
        return cur.fetchall()


def execute(query: LiteralString, params: tuple = ()) -> int:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()
        return cur.rowcount
