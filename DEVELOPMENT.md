# CloudStudent Local Development Guide

Follow these steps to set up the CloudStudent platform securely on your local machine.

## Prerequisites
- **Git**
- **Docker** and **Docker Compose**
- **Python 3.12** (Optional, only if running outside Docker for IDE integration)

## 1. Clone Repository
```bash
git clone https://github.com/LakshayYadav167/cloudstudent.git
cd cloudstudent
```

## 2. Create Environment File
Copy the example environment variables to create your local `.env`.
```bash
cp .env.example .env
```
Ensure you update any dummy values if desired, though the defaults in `.env.example` are generally sufficient for local Dockerized development.

**Never commit the `.env` file to version control.**

### Important Environment Variables
| Variable | Purpose | Required | Example |
|----------|---------|----------|---------|
| `DJANGO_SECRET_KEY` | Core Django cryptographic key | Yes | `django-insecure-dev-key` |
| `DJANGO_DEBUG` | Enables stack traces and debug tools | Yes (Local) | `True` |
| `DATABASE_URL` | PostgreSQL connection string | Yes | `postgres://user:pass@db:5432/db` |
| `ALLOWED_HOSTS` | Hosts permitted to access Django | Yes | `localhost,127.0.0.1` |

## 3. Run the Application
Use Docker Compose to build the containers, run migrations natively, and launch Gunicorn.
```bash
docker compose up --build
```

Wait until you see the Gunicorn workers booting up and `Listening at: http://0.0.0.0:8000`.

## 4. Run Migrations (If Needed)
Migrations run automatically on boot via the Docker `command`. To run them manually:
```bash
docker compose exec web python manage.py migrate
```

## 5. Create Demo / Seed Data
Create a superuser to access the Django admin panel:
```bash
docker compose exec web python manage.py createsuperuser
```
(Follow the interactive prompts).

## 6. Accessing the Application
- **Web UI**: [http://localhost:8000](http://localhost:8000)
- **Django Admin**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **API Root**: [http://localhost:8000/api/](http://localhost:8000/api/)

## 7. Development Workflow
1. Create a new feature branch (`git checkout -b feature/xyz`).
2. Make your code changes.
3. Verify Django system checks: `docker compose exec web python manage.py check`
4. Run tests (See [TESTING.md](TESTING.md)).
5. Commit and push. GitHub Actions will automatically verify the build.
