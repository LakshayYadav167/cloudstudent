# CloudStudent Docker Deployment Guide

This document outlines the steps to build, run, and manage the CloudStudent platform using Docker and Docker Compose for production-like environments.

## 1. Prerequisites
- **Docker Engine** (v20.10 or newer)
- **Docker Compose** (v2.0 or newer)
- Git (optional, for version control)

*Note on Python Version:* The project's default Python 3.14 environment is currently incompatible with Django 5.0.3's template context copying mechanism (raising `AttributeError` during template rendering). To ensure stability without silently upgrading major dependencies, the production container explicitly targets **Python 3.12** (`python:3.12-slim`), which provides full LTS compatibility with our locked dependencies.

## 2. Environment Setup
Create a `.env` file from the provided example to hold your secrets and configuration variables:
```bash
cp .env.example .env
```
Edit the `.env` file to customize:
- `SECRET_KEY` (must be strong and secret)
- `DEBUG` (set to `False` in production)
- Database credentials (if modifying defaults)

## 3. Building the Image
Build the Docker image using Compose. This step resolves dependencies and sets up the container:
```bash
docker compose build
```

## 4. Starting Services
Start the PostgreSQL database and Django web server in detached mode:
```bash
docker compose up -d
```
The web service uses `depends_on` with a `service_healthy` check to ensure it only starts after PostgreSQL is fully initialized.

## 5. Stopping Services
To safely stop the containers without destroying data:
```bash
docker compose stop
```
To bring down the containers entirely:
```bash
docker compose down
```

## 6. Viewing Logs
Check the application and database logs for monitoring and debugging:
```bash
# Both services
docker compose logs -f

# Web service only
docker compose logs -f web

# DB service only
docker compose logs -f db
```

## 7. Running Migrations
**Warning:** Destructive commands are *never* run automatically on startup.
To safely apply existing migrations in production:
```bash
docker compose exec web python manage.py migrate
```

## 8. Running Tests
You can run the full test suite inside the container environment to ensure correctness:
```bash
docker compose exec web python -m pytest
```

## 9. Accessing Django Admin
The Django Admin panel is available at:
`http://localhost:8000/admin/`

## 10. Accessing the API
The REST API endpoints (e.g., Students, Courses, Dashboard) are available starting at:
`http://localhost:8000/api/`

## 11. Health Endpoint
A lightweight health endpoint is available to check application status:
`http://localhost:8000/health/`

## 12. Database Persistence
PostgreSQL data is stored securely in a named volume (`postgres_data`).
Data persists across `docker compose restart`, `docker compose stop`, and `docker compose down`.
*(Do not use `docker compose down -v` unless you explicitly intend to delete your data).*

## 13. Static Files
In this configuration, static files are collected dynamically via the startup command (`collectstatic`). They are served seamlessly and efficiently through Gunicorn utilizing the **WhiteNoise** middleware, which provides automatic compression and caching headers.

## 14. Troubleshooting
- **Database Connection Error:** Ensure the `db` service is healthy (`docker compose ps`). Check that your `DATABASE_URL` matches your `POSTGRES_*` environment variables.
- **Static Files Missing:** Ensure `collectstatic` successfully ran. You can manually run it via `docker compose exec web python manage.py collectstatic --noinput`.
- **Bad Gateway (502):** Usually means Gunicorn failed to start. Check logs via `docker compose logs web`.
