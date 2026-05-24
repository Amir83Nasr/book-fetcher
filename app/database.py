"""Database connection pool using psycopg2.

Why connection pooling?
- Creating a new connection is expensive (TCP handshake, authentication)
- Connection pool reuses existing connections
- Handles broken connections automatically
- Limits maximum concurrent connections
"""

from contextlib import contextmanager
from typing import Any

from psycopg2 import pool
from psycopg2.extras import RealDictCursor

from app.config import settings

# Thread-safe connection pool
# minconn: minimum connections kept ready
# maxconn: maximum connections allowed
connection_pool = pool.ThreadedConnectionPool(
    minconn=settings.DB_MIN_CONN,
    maxconn=settings.DB_MAX_CONN,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
    user=settings.DB_USER,
    password=settings.DB_PASS,
)


@contextmanager
def get_cursor(cursor_factory=RealDictCursor):
    """Get a database cursor from the connection pool.

    Uses context manager to ensure connections are returned to pool.
    RealDictCursor returns rows as dictionaries with column names.

    Usage:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM books")
            rows = cur.fetchall()
    """
    conn = connection_pool.getconn()
    try:
        with conn.cursor(cursor_factory=cursor_factory) as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        connection_pool.putconn(conn)


def execute_query(
    query: str,
    params: tuple = None,
    fetch_one: bool = False,
    fetch_all: bool = True,
) -> list[dict[str, Any]] | dict[str, Any] | None:
    """Execute a SQL query and return results.

    Args:
        query: SQL query string with %s placeholders
        params: Tuple of parameters for the query
        fetch_one: If True, return single dict instead of list
        fetch_all: If False, don't fetch results (for INSERT/UPDATE/DELETE)

    Returns:
        - List of dictionaries for SELECT with fetch_all=True
        - Single dictionary for SELECT with fetch_one=True
        - None for INSERT/UPDATE/DELETE (when fetch_all=False)
    """
    with get_cursor() as cur:
        cur.execute(query, params)

        # If cursor has no description, it's not a SELECT query
        if cur.description is None:
            return None

        # If we don't want to fetch, return None
        if not fetch_all:
            return None

        # Fetch results
        if fetch_one:
            return cur.fetchone()
        return cur.fetchall()
