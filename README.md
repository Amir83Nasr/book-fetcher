# Book API

A high-performance book search API built with **FastAPI**, **PostgreSQL**, and **Redis caching**. Features include full-text search, pagination, author analytics, and load testing capabilities.

## Features

- Search books by title, author, or publisher (case-insensitive)
- Search authors with book counts
- Add new books with automatic author creation
- Redis caching with configurable TTL
- Connection pooling for PostgreSQL
- Pagination on all list/search endpoints
- Load testing with Locust
- Fully typed with mypy validation

## Tech Stack

| Technology | Purpose                |
|----------- |------------------------|
| FastAPI    | Web framework          |
| PostgreSQL | Relational database.   |
| Redis      | In-memory cache        |
| Docker     | Containerized services |
| Locust     | Load testing           |
| Pydantic   | Data validation        |

## Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose

### Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd book-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Start PostgreSQL & Redis
make up

# Create tables and seed sample data
make seed

# Generate massive test data (optional)
python scripts/generate_mock_data.py

# Start the server
make run
```

API is now running at **<http://localhost:8000>**  
Swagger docs at **<http://localhost:8000/docs>**

### Stop Services

```bash
# Stop API server: Ctrl+C
# Stop databases (data persists):
make down

# Stop and remove all data:
make clean
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/books` | List all books (paginated) |
| `GET` | `/books/search?q=ring` | Search books (cached) |
| `POST` | `/books` | Add a new book |
| `GET` | `/authors/search?q=orwell` | Search authors with book count |
| `GET` | `/cache/clear` | Clear Redis cache |

### Example Responses

**Search Books:**

```json
{
  "query": "ring",
  "total": 3,
  "page": 1,
  "page_size": 5,
  "total_pages": 1,
  "results": [
    {
      "id": 6,
      "title": "The Lord of the Rings",
      "author": "J.R.R. Tolkien",
      "year": 1954,
      "publisher": "Allen & Unwin"
    }
  ],
  "from_cache": true
}
```

**Search Authors:**

```json
{
  "query": "orwell",
  "results": [
    {
      "name": "George Orwell",
      "book_count": 2
    }
  ],
  "from_cache": false
}
```

## Project Structure

```txt
book-api/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings (pydantic-settings)
│   ├── database.py          # Connection pool
│   ├── cache.py             # Redis helpers
│   ├── models/
│   │   ├── book.py          # Pydantic models
│   │   └── author.py
│   ├── routers/
│   │   ├── books.py         # Book endpoints
│   │   └── authors.py       # Author endpoints
│   └── db/
│       └── queries.py       # SQL queries
├── scripts/
│   ├── seed_db.py           # Initial data
│   └── generate_mock_data.py  # Massive test data
├── tests/
│   └── locustfile.py        # Load test scenarios
├── docs/
│   └── locust/
│       ├── no-cache/        # Load test reports (no cache)
│       └── cache/           # Load test reports (with cache)
├── docker-compose.yml       # PostgreSQL + Redis
├── Makefile                 # Task shortcuts
└── .env.example             # Environment template
```

## Load Testing

### Run Tests

```bash
# Without cache
curl -s http://localhost:8000/cache/clear
locust -f tests/locustfile.py \
  --host=http://localhost:8000 \
  --users=100 \
  --spawn-rate=10 \
  --run-time=60s \
  --headless \
  --html=docs/locust/no-cache/report.html \
  --csv=docs/locust/no-cache/results

# With cache (run immediately after)
locust -f tests/locustfile.py \
  --host=http://localhost:8000 \
  --users=100 \
  --spawn-rate=10 \
  --run-time=60s \
  --headless \
  --html=docs/locust/cache/report.html \
  --csv=docs/locust/cache/results
```

### View Reports

Open the HTML files in your browser:

```bash
open docs/locust/no-cache/report.html
open docs/locust/cache/report.html
```

### Expected Results

| Metric | No Cache | With Cache |
|--------|----------|------------|
| RPS | ~40 | ~300+ |
| Avg Response | ~2000ms | ~15ms |
| 95th Percentile | ~5000ms | ~50ms |

## Environment Variables

Copy `.env.example` to `.env` and adjust values:

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | localhost | PostgreSQL host |
| `DB_PORT` | 5432 | PostgreSQL port |
| `DB_NAME` | bookdb | Database name |
| `DB_USER` | postgres | Database user |
| `DB_PASS` | - | Database password |
| `REDIS_HOST` | localhost | Redis host |
| `REDIS_PORT` | 6379 | Redis port |
| `REDIS_CACHE_TTL` | 300 | Cache TTL in seconds |

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all commands |
| `make up` | Start PostgreSQL & Redis |
| `make down` | Stop services |
| `make seed` | Create tables & seed data |
| `make run` | Start FastAPI server |
| `make locust` | Open Locust UI |
| `make lint` | Lint code |
| `make format` | Format code |
| `make typecheck` | Run mypy |
| `make clean` | Remove everything |
