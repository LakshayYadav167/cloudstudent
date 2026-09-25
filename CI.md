# CloudStudent CI/CD Documentation

This document outlines the Continuous Integration (CI) pipeline for the CloudStudent platform, configured using GitHub Actions.

## 1. Trigger Configuration
The CI pipeline (`.github/workflows/ci.yml`) is automatically triggered on:
- **Push** to `main` and `master` branches
- **Pull Request** against `main` and `master` branches

## 2. What the CI Pipeline Validates
The workflow ensures that all code merged into the production branches is structurally sound, passes all automated tests, and can be containerized successfully. Specifically, it executes:
- **Dependency Installation**: Caches and installs dependencies from `requirements.txt`.
- **Django System Checks**: Runs `python manage.py check` to catch structural or configuration errors.
- **Migration Verification**: Runs `python manage.py migrate --noinput` against a fresh database to ensure all migration files are valid and conflict-free.
- **Test Suite**: Executes the complete `pytest` suite (Model, UI/View, and API tests).
- **Docker Build Validation**: Builds the production Docker image to ensure the `Dockerfile` remains fully buildable.

## 3. Environment Specs
- **Runner**: `ubuntu-latest`
- **Python Version**: 3.12 (matches our production container requirement)
- **Database**: PostgreSQL 15 (spun up as a GitHub Actions service container)

## 4. Expected Successful Result
A successful run will complete all steps without errors. The expected test baseline is:
- **26 tests passed**
- **0 failed**
- **0 errors**

The Docker build step must conclude with a successfully tagged `cloudstudent:test` image.

## 5. Security & Credentials
- **No production secrets** are stored or used in the workflow.
- A dummy, test-only `SECRET_KEY` is injected strictly via the workflow's local `env` block.
- The `DATABASE_URL` strictly points to the ephemeral PostgreSQL service container spun up exclusively for the CI run.
- Azure deployment credentials and registry tokens are specifically excluded from this phase.

## 6. Where to View Results
You can view the real-time execution and historical results of these CI runs in the **Actions** tab of your GitHub repository. Any failure in the pipeline will visibly flag the associated pull request or commit as failed.
