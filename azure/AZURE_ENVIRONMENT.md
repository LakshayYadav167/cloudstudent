# Azure Environment Configuration Blueprint

This document outlines the environment variables required to run CloudStudent in Azure App Service. **No real secrets are committed to this repository.**

| Variable | Purpose | Sensitive? | Where to Configure |
|----------|---------|------------|--------------------|
| `SECRET_KEY` | Cryptographic signing key for Django sessions and tokens. | **YES** | `<SET-IN-AZURE-APP-SETTINGS>` |
| `DEBUG` | Controls error reporting. Must be `False` in production to prevent stack trace leaks. | NO | `<SET-IN-AZURE-APP-SETTINGS>` |
| `DATABASE_URL` | Connection string for PostgreSQL. Formatted for `dj-database-url`. | **YES** | `<SET-IN-AZURE-APP-SETTINGS>` |
| `ALLOWED_HOSTS` | Whitelist of domains allowed to serve the application (e.g. `app-cloudstudent-prod.azurewebsites.net`). | NO | `<SET-IN-AZURE-APP-SETTINGS>` |
| `CSRF_TRUSTED_ORIGINS` | Required for secure form submission over HTTPS. | NO | `<SET-IN-AZURE-APP-SETTINGS>` |
| `PORT` / `WEBSITES_PORT` | The port Gunicorn should bind to inside the container. Usually injected by Azure (defaults to 8000). | NO | Azure Environment Defaults / App Settings |

## Why these must not be committed:
Committing the `SECRET_KEY` or `DATABASE_URL` would expose the production application to cryptographic attacks and full database breaches. The 12-factor methodology explicitly dictates that environment configuration must remain strictly isolated from source control.
