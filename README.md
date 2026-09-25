# CloudStudent

A modern, role-based educational management system and web application built with Django, Django REST Framework (DRF), and PostgreSQL. 

CloudStudent provides a comprehensive dashboard and API ecosystem for administrating courses, enrollments, students, and academic records.

## Features
- **Role-Based Access Control (RBAC):** Distinct interfaces and strict data isolation for `ADMIN`, `TEACHER`, and `STUDENT` roles.
- **REST API:** Fully featured DRF endpoints with Token Authentication, pagination, and filtering.
- **Academic Management:** End-to-end management of Students, Courses, Enrollments, and Grades/Attendance.
- **Dynamic Dashboards:** Context-aware data visualization tailored to the user's role.
- **Containerized Architecture:** Fully production-ready Docker and `docker-compose` environment.
- **Automated CI/CD:** Hardened GitHub Actions pipeline enforcing code quality, database migration integrity, and test coverage on all PRs.

## Technology Stack
- **Backend:** Python 3.12, Django 5.0, Django REST Framework
- **Database:** PostgreSQL 15
- **Frontend:** HTML5, CSS3, Bootstrap 5, Vanilla JavaScript
- **Infrastructure:** Docker, Gunicorn, WhiteNoise (Static Files)
- **CI/CD:** GitHub Actions, Pytest

## Local Development Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/LakshayYadav167/cloudstudent.git
   cd cloudstudent
   ```
2. **Environment Configuration:**
   Copy `.env.example` to `.env` and fill in the required variables.

3. **Start the application with Docker:**
   ```bash
   docker compose up --build
   ```
   The application will be accessible at `http://localhost:8000`.

4. **Run Tests:**
   ```bash
   docker compose exec web python -m pytest
   ```

## Documentation
- [Architecture Details](ARCHITECTURE.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Docker Setup](DOCKER.md)
- [Continuous Integration (CI)](CI.md)
- [Azure Deployment Plan](AZURE_DEPLOYMENT.md)

## License
This project is licensed under the MIT License.
