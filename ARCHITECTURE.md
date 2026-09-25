# Architecture Design: CloudStudent (Revised)

## 1. System Requirements Analysis
- **Goal:** Manage student records, courses, and academic information through a centralized online system.
- **Key Features:** Student registration, course creation, enrollment, grading (with automated logic), dashboard statistics, and REST API integrations.
- **Constraints:** Keep the architecture simple yet strictly production-ready for Azure deployment with PostgreSQL. Ensure robust database-level constraints.

## 2. Overall Architecture
- **Pattern:** Monolithic architecture with Django serving HTML templates for the web interface and exposing REST APIs (via DRF) for potential future decoupling or mobile client integration.
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript. Django templates for server-side rendering.
- **Backend:** Python 3.12, Django, Django REST Framework.
- **Database:** **PostgreSQL** is the primary supported database. Configuration is injected securely through the `DATABASE_URL` environment variable via `dj-database-url`. (SQLite is only an optional temporary fallback if `DATABASE_URL` is omitted locally).
- **Hosting:** Azure (Azure App Service for the web container, Azure Database for PostgreSQL).

## 3. Django Apps Required
- `accounts`: Handles Custom User Model, authentication, role management (Admin, Teacher, Student).
- `students`: Manages student-specific academic profiles and demographics.
- `courses`: Manages the course catalog and course enrollments.
- `academics`: Manages academic records, marks, attendance, and automated grade calculation.
- `dashboard`: Computes and serves system-wide statistics (total students, average marks, recent records) securely from the database.

## 4. Database Entities & Relationships
All models share common audit fields: `created_at` and `updated_at`.

- **User (Accounts App):** Extends Django's `AbstractUser`.
  - Fields: `role` (ADMIN, TEACHER, STUDENT choices), `phone`, `address`.
- **StudentProfile (Students App):** One-to-One relationship with `User`.
  - Fields: `enrollment_number` (Unique, Indexed), `date_of_birth`, `gender`, `department`, `program`, `semester`, `enrollment_date`, `status`.
- **Course (Courses App):**
  - Fields: `code` (Unique), `name`, `description`, `credits`, `department`, `semester`, `instructor` (ForeignKey to `User`).
- **Enrollment (Courses App):** Many-to-Many through-model linking `StudentProfile` and `Course`.
  - Fields: `academic_year`, `semester`, `enrollment_date`, `status`.
  - **Constraint:** `UniqueConstraint` on (student, course, academic_year, semester) to prevent duplicate enrollments.
- **AcademicRecord (Academics App):**
  - Fields: `student`, `course`, `enrollment` (One-to-One), `academic_year`, `semester`, `marks` (0-100), `attendance` (0-100), `grade` (Auto-calculated: A+, A, B, C, D, F).
  - **Constraint:** `UniqueConstraint` on (student, course, academic_year, semester).

## 5. Security & Configuration
- **Authentication:** Django session-based for Web Views, Token/JWT for API access.
- **Authorization:** Role-based checks against the User `role` field.
- **Configuration Management:** All sensitive variables (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`) are read from environment variables (`.env`). No hardcoded secrets.
- **Security:** Standard Django security features (CSRF protection, Password Hashing, X-Frame-Options).

## 6. Docker & CI/CD Architecture
- **Docker:** `web` service (Gunicorn) and `db` service (PostgreSQL).
- **GitHub Actions (CI/CD):** Triggers on push to `main`. Runs `flake8`/`black` and `pytest`. Builds and pushes Docker images to Azure Container Registry (ACR), triggering an Azure App Service webhook.

## 7. Azure Deployment Architecture
- **Web Hosting:** Azure App Service (Web App for Containers).
- **Database:** Azure Database for PostgreSQL - Flexible Server.
- **Storage:** Azure Blob Storage for static/media files (`django-storages`).
