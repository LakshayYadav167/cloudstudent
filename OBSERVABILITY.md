# CloudStudent Observability

This document details the Zero-Cost Observability & Logging architecture implemented in CloudStudent. It leverages standard Python, Django, and Docker capabilities to provide production-ready insights without requiring paid third-party monitoring services (such as Azure Monitor, Datadog, or Grafana).

## Logging Architecture
CloudStudent uses Python's standard `logging` library integrated seamlessly with Django's logging framework. The configuration is centralized in `settings.py` via the `LOGGING` dictionary. All logs are directed to `console` (stdout/stderr), which is the standard, best-practice approach for Dockerized applications.

## Log Levels
Logging behavior is environment-aware:
- **DEBUG**: Enabled only when `DEBUG=True`. Emits fine-grained application logs.
- **INFO**: The standard production log level. Emits requests, successful security events, and general flow.
- **WARNING**: Emits on 4xx Client Errors and failed security/authentication events.
- **ERROR / CRITICAL**: Emits on 5xx Server Errors and unhandled exceptions.

## Request Logging
The application uses a custom `RequestLoggingMiddleware`. It automatically intercepts every HTTP request (except `/health/` to avoid spam) and emits a single, structured log entry on response.
Format:
```text
method=GET path=/api/students/ status=200 duration=45.2ms user=admin_user request_id=b56c...
```

## Error Logging
- **Client Errors (4xx)**: Handled gracefully and logged at the `WARNING` level with the exact path and user.
- **Server Errors (5xx)**: Logged at the `ERROR` level by the middleware. Django's core `django.request` logger also captures unhandled exceptions. Note: Stack traces are NEVER returned to the client in production.

## Authentication/Security Events
Security events are captured efficiently via Django Signals (`user_logged_in` and `user_login_failed`) and logged using the `cloudstudent.security` logger.
- Successful logins log the username and request ID at the `INFO` level.
- Failed attempts log the attempted username (safely extracted from credentials) at the `WARNING` level. Passwords are mathematically guaranteed never to be logged.

## Request Correlation
The middleware automatically injects a unique `uuid4` into every request as `request.request_id`. This ID is appended to all request and security logs, allowing developers to trace the entire lifecycle of a specific request. The ID is also returned to the client via the `X-Request-ID` HTTP header for easier bug reporting.

## Docker Logs
Docker naturally captures all `stdout` and `stderr` streams emitted by the container. 
To view production application logs locally, use:
```bash
docker compose logs web
```
To tail logs in real-time:
```bash
docker compose logs -f web
```

## Gunicorn Logs
Gunicorn is natively configured to push access and error logs to the Docker console output alongside the Django application logs, providing a unified stream of WSGI-level and App-level events.

## Health Endpoint
The `/health/` endpoint is located at `cloudstudent/urls.py`. It explicitly verifies database connectivity using `django.db.connection.ensure_connection()`.
- Returns HTTP 200 `{'status': 'ok', 'database': 'connected'}` when healthy.
- Returns HTTP 503 `{'status': 'error', 'database': 'disconnected'}` if the database is unreachable, avoiding silent failures in orchestration environments.

## Sensitive Data Protection
A strict sanitization policy is enforced:
- Passwords, `Authorization` headers, session cookies, and the `SECRET_KEY` are NEVER logged.
- The `POST` body payload is never dumped to the log stream to prevent accidental PII leakage.
- Security events extract ONLY the `username` from credentials dictionaries.

## Local Debugging
During local development, running `docker compose up` will output the cleanly formatted logs directly to your terminal. Errors will show up distinctively due to Django's standard formatting.

## Production Considerations
For production, standard Docker log rotation applies. Do NOT configure Django to write to local flat files (`.log`), as container file systems are ephemeral.

## Future Cloud Integration
While this project remains strictly at a **₹0 budget** with no paid cloud services provisioned, this architecture is forward-compatible. If deployed to Azure App Service in the future, these standard `stdout` logs will automatically stream into Azure Log Analytics or Application Insights with zero code changes required.
