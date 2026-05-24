"""SQL queries as constants.

Keeping queries separate from endpoints makes code cleaner
and easier to maintain.
"""

# ========== Table Creation ==========

CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author_id INTEGER REFERENCES authors(id),
    year INTEGER CHECK (year >= 1000 AND year <= 2026),
    publisher VARCHAR(100)
);
"""

# ========== Books ==========

GET_ALL_BOOKS = """
    SELECT b.id, b.title, a.name AS author, b.year, b.publisher,
           COUNT(*) OVER() AS total_count
    FROM books b
    INNER JOIN authors a ON b.author_id = a.id
    ORDER BY b.title
    LIMIT %s OFFSET %s
"""

SEARCH_BOOKS = """
    SELECT b.id, b.title, a.name AS author, b.year, b.publisher,
           COUNT(*) OVER() AS total_count
    FROM books b
    INNER JOIN authors a ON b.author_id = a.id
    WHERE b.title ILIKE %s OR a.name ILIKE %s OR b.publisher ILIKE %s
    ORDER BY b.title
    LIMIT %s OFFSET %s
"""

INSERT_BOOK = """
    INSERT INTO books (title, author_id, year, publisher)
    VALUES (%s, %s, %s, %s)
    RETURNING id, title, (SELECT name FROM authors WHERE id = %s) AS author, year, publisher
"""

# ========== Authors ==========

SEARCH_AUTHORS = """
    SELECT a.name, COUNT(b.id) AS book_count
    FROM authors a
    LEFT JOIN books b ON a.id = b.author_id
    WHERE a.name ILIKE %s
    GROUP BY a.id, a.name
    ORDER BY book_count DESC
"""

GET_OR_CREATE_AUTHOR = """
    INSERT INTO authors (name)
    VALUES (%s)
    ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
    RETURNING id
"""
