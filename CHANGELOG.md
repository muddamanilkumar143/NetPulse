# Changelog

## [0.3.0] - 2026-11-27

- Added MongoDB persistence with startup collection indexes while retaining
  in-memory and MySQL backends.
- Added backward-compatible optional device location support across repositories.
- Updated MongoDB driver support to PyMongo 4.20.2.

## [0.2.0] - 2026-11-27

- Completed the FastAPI device-monitoring baseline: validated device and alert
  schemas, REST endpoints, in-memory repository, online-to-offline alert
  handling, API contract examples, and automated service tests (Steps 1-8).
- Added configurable MySQL persistence with SQLAlchemy and PyMySQL while
  retaining the in-memory repository for isolated tests (Steps 9-10 and 12).
- Added Alembic migrations for the initial devices and alerts schema and the
  subsequent optional device location field (Steps 11 and 13).
- Added GitHub Actions test automation.