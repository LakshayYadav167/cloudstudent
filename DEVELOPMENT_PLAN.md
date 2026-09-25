# Phased Development Plan: CloudStudent (Revised)

## Phase 1: Planning & Setup (Current)
- Analyze requirements and finalize technology stack.
- Design architecture, database entities, and strict database constraints.
- Emphasize PostgreSQL as the primary database architecture.
- Initialize Django project and apps (`accounts`, `students`, `courses`, `academics`, `dashboard`).
- Secure settings with environment variables (`DATABASE_URL`, `SECRET_KEY`, etc.).
- Complete Phase 1 review to ensure compliance with production requirements.

## Phase 2: Core Models & Database
- Implement the Custom User model with Role choices in the `accounts` app.
- Ensure `AUTH_USER_MODEL` is correctly bound before running `makemigrations`.
- Create models for `students`, `courses`, and `academics` apps with `UniqueConstraints` and validators.
- Setup PostgreSQL locally via Docker Compose or native installation.
- Generate and apply initial database migrations carefully.
- Configure the Django Admin interface to manage these models.

## Phase 3: Web Views & Templates (Frontend)
- Integrate Bootstrap 5 static files and assets.
- Create a base template layout (navbar, sidebar, footer).
- Implement Home, Login, Registration, and Dashboard pages (fetching live stats from DB).
- Implement Views and Templates for the Course Catalog, Enrollments, and Academic Records.
- Apply role-based access control based on the User `role` field.

## Phase 4: REST API Integration & Testing
- Install and configure Django REST Framework (DRF).
- Create serializers and viewsets for Courses, Students, and Academics.
- Add authentication (Token/JWT) for API access.
- Write unit and integration tests using `pytest` and the Django Test Framework.

## Phase 5: Containerization & DevOps
- Write the `Dockerfile` for the Django web service.
- Finalize `docker-compose.yml` for multi-container local setup (web, db).
- Implement robust configuration management (handling `SECRET_KEY` and DB settings via env vars).
- Setup the GitHub Actions workflow for automated testing and linting (CI).

## Phase 6: Cloud Deployment (Azure)
- Provision Azure Database for PostgreSQL.
- Provision Azure App Service (Web App for Containers).
- Configure Azure Blob Storage and `django-storages` for static and media files.
- Extend GitHub Actions to build and push Docker images, triggering CD to Azure.
- Perform final end-to-end testing and production release.
