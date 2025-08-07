# Backend

This backend will be built using FastAPI to provide RESTful endpoints and handle data ingestion from dark-web sources. The architecture follows a microservice approach with separate components for crawling, analysis, alerting, and integrations.

## Directory structure

- `app/main.py` – entry point for the FastAPI application.
- `app/api` – API route definitions.
- `app/core` – core services such as crawlers, parsers, and machine learning modules.
- `app/models` – data models and database ORM definitions.

Further modules will be added as development progresses.
