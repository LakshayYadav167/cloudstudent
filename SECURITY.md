# CloudStudent Security

This document outlines the security controls, validations, and architectural decisions made to harden the CloudStudent platform.

## Authentication
CloudStudent uses Django's native session authentication for web views and Token Authentication (`rest_framework.authtoken`) for the REST API. Session cookies are protected against tampering.

## Authorization
A strict Role-Based Access Control (RBAC) model is enforced server-side.
- **ADMIN**: Unrestricted access.
- **TEACHER**: Can only create/update/delete Academic Records for courses they instruct. Can view enrollments and records associated with their courses.
- **STUDENT**: Strictly read-only access limited exclusively to their own enrollments, academic records, and dashboard data.

## Object-Level Data Isolation (IDOR/BOLA Protection)
All primary ModelViewSets (API) and Django Class-Based Views (HTML) explicitly filter querysets based on `request.user`. Even if a malicious actor acquires the numeric primary key (ID) of an unauthorized resource, the backend will return a generic `404 Not Found` or `403 Forbidden` response, mathematically preventing Insecure Direct Object References (IDOR).

## API Security
- Unauthenticated API access is universally blocked (`401 Unauthorized`).
- Pagination is enforced globally (`PAGE_SIZE=10`) to prevent denial-of-service through excessive database fetches.
- Non-admin users are strictly blocked from writing to administrative API endpoints (`IsAdminOrReadOnly` custom permission).

## Input Validation
Django REST Framework serializers and Django native model validators enforce strict boundaries on numeric fields (e.g., Marks between 0-100, Attendance between 0-100). Malformed JSON drops instantly as a `400 Bad Request` before ever hitting the ORM.

## CSRF Protection
Cross-Site Request Forgery (CSRF) is enabled natively for all session-based HTML views. `CSRF_TRUSTED_ORIGINS` is restricted tightly via environment variables.

## Session and Cookie Security
In production, standard security parameters are engaged:
- `SESSION_COOKIE_HTTPONLY=True`
- `CSRF_COOKIE_HTTPONLY=True`
- `SESSION_COOKIE_SECURE=True` (If HTTPS enabled)
- `CSRF_COOKIE_SECURE=True` (If HTTPS enabled)

## Security Headers
The following HTTP security headers are natively enforced:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` (Prevent Clickjacking)
- `Referrer-Policy: same-origin`
- `Strict-Transport-Security` (HSTS) with Preload is fully supported and environment-aware for production deployment.

## Secret Management
The codebase strictly adheres to the 12-factor methodology. All sensitive properties (`SECRET_KEY`, `DATABASE_URL`, admin credentials) are loaded asynchronously via `.env` files locally or App Settings in the cloud. No secrets have been committed to this repository.

## Docker Security
The Dockerfile is built upon the minimal `python:3.12-slim` image to reduce the attack surface. It excludes unnecessary OS packages, relies completely on standardized wheels, and is completely read-only against the host system outside of declared volumes.

## Dependency Security
Dependencies are pinned directly in `requirements.txt` (`Django==5.0.3`). Regular maintenance and CVE monitoring should be performed manually. Automated dependency bumps are avoided to ensure mathematical stability of the monolithic architecture.

## Error Handling
Stack traces are fundamentally disabled in production (`DEBUG=False`). Internal 500 errors display generic HTML/JSON to the client, while preserving the full diagnostic stack trace locally in `stdout` for the operational team.

## Logging Security
The observability layer is carefully sanitized. Database passwords, authorization tokens, session cookies, and entire POST request bodies are **never** evaluated by the standard Python logger. Failed logins only log the requested `username`, preventing accidental credential logging (when users mistakenly paste their password into the username field).

## Known Limitations
- Rate-limiting (Throttling) has not been implemented at the Django layer to avoid overengineering. In a genuine deployment, an Nginx reverse-proxy or Azure App Gateway should provide WAF rate-limiting.
- A broad Content-Security-Policy (CSP) has not been added to avoid breaking the core Bootstrap 5 UI/UX integration.

## Future Improvements
- Migration to Redis-backed caching for the API.
- Native integration with a Web Application Firewall (WAF).
