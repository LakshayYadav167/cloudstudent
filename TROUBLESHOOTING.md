# Troubleshooting Guide

Common issues encountered when running CloudStudent locally via Docker.

## 1. PostgreSQL Unavailable / Connection Refused
**Symptom**: `OperationalError: could not connect to server: Connection refused`
**Fix**: The database container may not have finished initializing. Stop the containers (`docker compose down`) and bring them back up. PostgreSQL often takes 5-10 seconds to create the initial database files.

## 2. Port Already in Use
**Symptom**: `Error starting userland proxy: listen tcp4 0.0.0.0:8000: bind: address already in use`
**Fix**: Another application (or an orphaned CloudStudent container) is using port 8000. 
Find and stop the conflicting process, or modify `docker-compose.yml` to bind to a different host port (e.g. `8080:8000`).

## 3. Static Files Not Loading (404)
**Symptom**: The UI appears broken, lacking CSS styles.
**Fix**: Ensure `collectstatic` was run successfully. WhiteNoise requires static files to be collected into the `staticfiles` directory.
Run:
```bash
docker compose exec web python manage.py collectstatic --noinput
```

## 4. Test Failures / HTTPS Redirects
**Symptom**: Pytest returns `301` or `302` redirects unexpectedly instead of `200` OK.
**Fix**: Ensure `SECURE_SSL_REDIRECT` is safely disabled in your test environment. In local Docker, this is configured via `DEBUG=True` or explicitly omitting the `SECURE_SSL_REDIRECT` environment variable.

## 5. Migrations Error
**Symptom**: `django.db.utils.ProgrammingError: relation "students_studentprofile" does not exist`
**Fix**: Database schema drift. Execute migrations:
```bash
docker compose exec web python manage.py migrate
```

## 6. Token Authentication Issues
**Symptom**: API returns `401 Unauthorized`.
**Fix**: Ensure you are passing the Authorization header exactly as `Authorization: Token <YOUR_TOKEN>`. Also ensure the user role associated with the token has sufficient permissions for the endpoint.
