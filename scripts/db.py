"""Database management script.

Usage:
    python scripts/db.py seed      # Create tables + 14 books (first time)
    python scripts/db.py reset     # Drop everything + 14 books (clean start)
    python scripts/db.py populate  # Add 10,000 random books (load test)
    python scripts/db.py status    # Show current counts
"""

import sys
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from app.database import execute_query

# Sample data
AUTHORS = [
    ("George Orwell", "United Kingdom"),
    ("Harper Lee", "United States"),
    ("Jane Austen", "United Kingdom"),
    ("J.R.R. Tolkien", "United Kingdom"),
    ("Gabriel Garcia Marquez", "Colombia"),
    ("Leo Tolstoy", "Russia"),
    ("F. Scott Fitzgerald", "United States"),
    ("Markus Zusak", "Australia"),
]

BOOKS = [
    ("1984", 1, 1949, "Secker & Warburg"),
    ("Animal Farm", 1, 1945, "Secker & Warburg"),
    ("To Kill a Mockingbird", 2, 1960, "J.B. Lippincott & Co."),
    ("Pride and Prejudice", 3, 1813, "T. Egerton"),
    ("The Hobbit", 4, 1937, "Allen & Unwin"),
    ("The Lord of the Rings", 4, 1954, "Allen & Unwin"),
    ("The Silmarillion", 4, 1977, "Allen & Unwin"),
    ("One Hundred Years of Solitude", 5, 1967, "Harper & Row"),
    ("Love in the Time of Cholera", 5, 1985, "Editorial Oveja Negra"),
    ("War and Peace", 6, 1869, "The Russian Messenger"),
    ("Anna Karenina", 6, 1877, "The Russian Messenger"),
    ("The Great Gatsby", 7, 1925, "Scribner"),
    ("Tender Is the Night", 7, 1934, "Scribner"),
    ("The Book Thief", 8, 2005, "Picador"),
]

# Mock data generators
FIRST_NAMES = ["James", "Mary", "Amir", "Sara", "Ali", "Fatemeh", "Omar", "Layla"]
LAST_NAMES = ["Smith", "Johnson", "Ahmadi", "Hosseini", "Rezaei", "Moradi"]
PUBLISHERS = ["Penguin", "HarperCollins", "Macmillan", "Random House", "Scholastic"]
ADJECTIVES = ["Lost", "Secret", "Dark", "Golden", "Fallen", "Eternal", "Ancient"]
NOUNS = ["Garden", "Kingdom", "Shadow", "Dream", "Storm", "Crown", "Sword"]


def create_tables():
    execute_query(
        """
        CREATE TABLE IF NOT EXISTS authors (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            country VARCHAR(50)
        );
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            author_id INTEGER REFERENCES authors(id),
            year INTEGER CHECK (year >= 1000 AND year <= 2026),
            publisher VARCHAR(100)
        );
    """,
        fetch_all=False,
    )


def drop_tables():
    execute_query("DROP TABLE IF EXISTS books CASCADE", fetch_all=False)
    execute_query("DROP TABLE IF EXISTS authors CASCADE", fetch_all=False)


def insert_sample_data():
    for name, country in AUTHORS:
        execute_query(
            "INSERT INTO authors (name, country) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (name, country),
            fetch_all=False,
        )
    for title, author_id, year, publisher in BOOKS:
        execute_query(
            "INSERT INTO books (title, author_id, year, publisher) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
            (title, author_id, year, publisher),
            fetch_all=False,
        )


def add_large(book_count=10_000, batch_size=500):
    authors = execute_query("SELECT id FROM authors")
    author_ids = [r["id"] for r in authors]

    for i in range(0, book_count, batch_size):
        batch = []
        for _ in range(batch_size):
            title = f"The {random.choice(ADJECTIVES)} {random.choice(NOUNS)}"
            author_id = random.choice(author_ids)
            year = random.randint(1800, 2024)
            publisher = random.choice(PUBLISHERS)
            batch.append((title, author_id, year, publisher))

        for b in batch:
            execute_query(
                "INSERT INTO books (title, author_id, year, publisher) VALUES (%s, %s, %s, %s)",
                b,
                fetch_all=False,
            )
        print(f"  {min(i + batch_size, book_count)}/{book_count} books inserted...")


def show_status():
    a = execute_query("SELECT COUNT(*) as c FROM authors", fetch_one=True)
    b = execute_query("SELECT COUNT(*) as c FROM books", fetch_one=True)
    print(f"  Authors: {a['c']}")
    print(f"  Books:   {b['c']}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/db.py [seed|reset|addsmall|addlarge|status]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "reset":
        print("Resetting database...")
        drop_tables()
        create_tables()
        show_status()

    elif cmd == "seed":
        print("Seeding database...")
        create_tables()
        show_status()

    elif cmd == "addsmall":
        print("Small with mock data...")
        insert_sample_data()
        show_status()

    elif cmd == "addlarge":
        print("Large with mock data...")
        insert_sample_data()
        add_large()
        show_status()

    elif cmd == "status":
        show_status()

    else:
        print(f"Unknown command: {cmd}")
        print("Usage: python scripts/db.py [seed|reset|addsmall|addlarge|status]")


if __name__ == "__main__":
    main()
