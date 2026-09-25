# Changelog

All notable changes to the CloudStudent project are documented here.

## [Unreleased] - 2026

### Architecture & Foundation
- Migrated primary database from SQLite to PostgreSQL 15.
- Containerized the entire application ecosystem with Docker and Docker Compose (Python 3.12-slim).
- Replaced the default development server with a production-grade WSGI Gunicorn setup.

### UI & UX
- Integrated Bootstrap 5 templates for responsive dashboard, course, and student views.

### Database & ORM
- Created custom `User` model with integrated `ADMIN`, `TEACHER`, and `STUDENT` roles.
- Implemented core domain models: `StudentProfile`, `Course`, `Enrollment`, `AcademicRecord`.

### API & Serializers
- Configured Django REST Framework (DRF) with token-based authentication.
- Exposed CRUD operations across all core modules via robust `ModelViewSet` classes.
- Added Search and Filtering integration for API consumers.

### CI/CD
- Established automated GitHub Actions CI pipeline executing Django checks, `pytest`, and Docker validation on `ubuntu-latest`.

### Observability
- Added custom `RequestLoggingMiddleware` for structured stdout/stderr logging.
- Introduced `X-Request-ID` tracing logic for request correlation.
- Wired Django Signals to log critical authentication events (success/failure) gracefully.

### Security
- Hardened Application against IDOR (Insecure Direct Object Reference) through strict `request.user` database filtering on APIs and Views.
- Implemented environment-aware HTTPS security parameters (HSTS, secure cookies).
- Enforced native HTTP Security Headers (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`).

### Azure Blueprint
- Established a comprehensive, zero-cost Azure Deployment Blueprint (Architecture Diagrams, CI/CD templates, guardrails). *Note: No active resources were provisioned.*
