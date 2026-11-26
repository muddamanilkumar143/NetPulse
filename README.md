# NetPulse

A small modular FastAPI network-device monitoring API. Device and alert state is held in memory and resets when the process restarts; this project does not contact devices or use a database.

## Run

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for the API, or check `GET /health`.

## Verify

```bash
python -m pytest -q
```

To see the alert transition, register a device with status `online`, patch its status to `offline` twice, then call `GET /alerts`. Only the first transition creates an alert. The example device in Swagger is `RTR-101`.

## Architecture

- Routes validate HTTP input and translate service errors into HTTP status codes.
- The service enforces registration and status-transition business rules.
- The repository owns in-memory device and alert storage and returns copies.
- The event function records an alert through the repository when the service detects an online-to-offline transition.

The repository is injected into the service, so a later storage adapter can implement the same repository operations without changing the service's business rules. The route, service, repository, and event modules are parts of one deployable modular monolith, not separate services.

FastAPI builds `/openapi.json` from the registered routes, their response metadata, and the Pydantic request and response models. Swagger UI at `/docs` renders that generated contract.