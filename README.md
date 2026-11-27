# NetPulse

A small modular FastAPI network-device monitoring API. It supports in-memory storage for quick runs and tests, or MySQL and MongoDB persistence. It does not contact monitored devices.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for the API, or check `GET /health`.

## Verify

```bash
python -m pytest -q
```

To see the alert transition, register a device with status `online`, patch its status to `offline` twice, then call `GET /alerts`. Only the first transition creates an alert. The example device in Swagger is `RTR-101`.

## MySQL

The app defaults to in-memory storage. To use MySQL, create a database and user, copy `.env.example` to `.env`, and set the MySQL credentials and `DATABASE_URL`. The `.env` file is ignored by Git.

```sql
CREATE DATABASE netpulse_db;
CREATE USER 'netpulse_user'@'localhost' IDENTIFIED BY 'change_me';
GRANT ALL PRIVILEGES ON netpulse_db.* TO 'netpulse_user'@'localhost';
```

With MySQL running and `.env` configured, apply the checked-in migrations and verify the current revision:

```bash
alembic history
alembic upgrade head
alembic current
```

The first migration creates `devices` and `alerts`; the next adds the nullable `location` column. To verify the reversible schema change, run `alembic downgrade -1` followed by `alembic upgrade head`. The API uses MySQL when `NETPULSE_STORAGE=mysql` is set; otherwise it continues to use the in-memory repository.

To create a later migration after changing the ORM models, use `alembic revision --autogenerate -m "describe schema change"`, review the generated migration, then apply it with `alembic upgrade head`.

## MongoDB

MongoDB `9.0.8` is the current stable server release used for this integration
(as of 2026-11-27). PyMongo `4.20.2` is the current driver release. Install a
MongoDB 9.0.8 server for your operating system, then configure `.env`:

```dotenv
NETPULSE_STORAGE=mongo
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=netpulse_db
DEVICES_COLLECTION=devices
ALERTS_COLLECTION=alerts
```

Start the API with `uvicorn app.main:app --reload`. Startup creates the device
and alert collections' indexes, including the unique device ID index. The
MongoDB adapter uses the same repository contract as the in-memory and MySQL
backends. Check the installed server with `mongod --version` and run the test
suite with `python -m pytest -q`.

## Architecture

- Routes validate HTTP input and translate service errors into HTTP status codes.
- The service enforces registration and status-transition business rules.
- The repository owns in-memory device and alert storage and returns copies.
- The event function records an alert through the repository when the service detects an online-to-offline transition.

The repository is injected into the service, so the in-memory, MySQL, and MongoDB adapters implement the same operations without changing the service's business rules. The route, service, repository, and event modules are parts of one deployable modular monolith, not separate services.

FastAPI builds `/openapi.json` from the registered routes, their response metadata, and the Pydantic request and response models. Swagger UI at `/docs` renders that generated contract.