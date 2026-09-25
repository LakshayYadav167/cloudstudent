# Contributing to CloudStudent

Thank you for considering contributing to CloudStudent! This is a student portfolio project emphasizing clean architecture, security, and developer experience.

## Coding Expectations
- Write readable, PEP-8 compliant Python.
- Follow Django Best Practices for "Fat Models, Skinny Views".
- Adhere to the strict Role-Based Access Control (RBAC) boundaries implemented in the existing views and serializers.

## Branch Workflow
1. Fork the repository.
2. Create a feature branch off `main`: `git checkout -b feature/your-feature-name`
3. Develop your feature.
4. Ensure all tests pass locally before committing.
5. Push to your branch and submit a Pull Request.

## Security Requirements
- **NO SECRETS**: Never commit `.env` files, production database passwords, API tokens, Azure credentials, or any cryptographic material.
- **Dependency Scope**: Do not introduce unnecessary dependencies, especially heavyweight tools like Redis, Celery, or external paid monitoring agents. The project has a strict **₹0 Cost Requirement**.
- **Data Isolation**: Any new endpoints must mathematically guarantee IDOR protections (filtering queries by `request.user`).

## Documentation Expectations
If your feature changes API boundaries, architecture, or environment variables, you **must** update the relevant Markdown files (`API_DOCUMENTATION.md`, `README.md`, `DEVELOPMENT.md`).

## Pull Request Expectations
- Title the PR clearly.
- Provide a summary of what changed and *why*.
- GitHub Actions CI will automatically run the pytest suite and Docker build against your branch. Your PR will only be reviewed if the CI pipeline is entirely green (Success).
