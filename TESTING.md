# Testing Guide

CloudStudent uses `pytest` and `pytest-django` to ensure the mathematical stability and security of the monolith.

## Executing Tests

To run the full test suite locally within the Docker container:
```bash
docker compose exec web python -m pytest
```

## Current Baseline
At the current project revision, the suite contains **44 tests**. All tests must pass successfully before a commit is pushed to the repository.

## Test Structure
Tests are located in the `tests/` directory:
- `test_models.py`: Validates ORM relationships, constraints, and cascading deletes.
- `test_views.py`: Validates HTML response codes, context data, and role-based access for Class-Based Views.
- `test_api.py`: Validates Django REST Framework Serializers, endpoints, query filtering, and token authentication.
- `test_security.py`: Verifies IDOR constraints, HTTP security headers, and data isolation logic.
- `test_observability.py`: Ensures `X-Request-ID` correlation and logging mechanisms function properly.

## Performance/Query Testing
We implicitly track database queries utilizing `pytest-django` assertion helpers (e.g., `django_assert_num_queries`) where appropriate to guard against regressions in the `select_related` / `prefetch_related` N+1 optimizations.

## Continuous Integration
Tests are automatically executed on Ubuntu runners via GitHub Actions on every `push` and `pull_request` to the `main` branch. See [CI.md](CI.md) for details.
