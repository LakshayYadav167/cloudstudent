# Azure Production Deployment Plan

## 1. Current Architecture Readiness
The project is structurally ready for Azure deployment via Docker. The application uses `django-environ` / `os.environ` to dynamically receive all configuration overrides required by Azure, eliminating hardcoded passwords. 

**Azure Compatibility Gap Resolved:** I have explicitly introduced `whitenoise` to our dependencies and middleware. Because Azure App Service for Containers routes *all* web traffic directly to Gunicorn, and Gunicorn is explicitly designed *not* to serve static files securely, Django will drop 404 errors on Bootstrap assets if `DEBUG=False`. `whitenoise` natively and efficiently resolves this from within the container.

## 2. Infrastructure Plan
The production environment will utilize:
1. **Azure Database for PostgreSQL Flexible Server**:
   - Version: 15
   - Tier: Burstable (B1ms for cost efficiency, scaling appropriately).
   - Firewall: Disallow public access except from Azure App Service outbound IPs or VNet Integration.
2. **Azure App Service (Web App for Containers)**:
   - Operating System: Linux
   - Image Source: GitHub Actions via Azure Container Registry (or Docker Hub).
   - Startup Command: Empty (handled by existing `CMD` inside our `Dockerfile`).
   - Exposed Port: `8000` (mapped natively via App Service App Settings `WEBSITES_PORT=8000`).

## 3. Required Application Settings (Environment Variables)
The following configuration variables will be explicitly securely mapped into the Azure App Service environment:
- `DEBUG=False`
- `SECRET_KEY=<Production Secure Key>`
- `DATABASE_URL=postgres://<admin>:<password>@<server>.postgres.database.azure.com:5432/<db>?sslmode=require`
- `ALLOWED_HOSTS=<app-name>.azurewebsites.net`
- `CSRF_TRUSTED_ORIGINS=https://<app-name>.azurewebsites.net`

## 4. Deployment Lifecycle
1. **Infrastructure Provisioning**: Create the flexible server and app service.
2. **Initial Database Verification**: Ensure the DB boots and networking correctly restricts internet traffic.
3. **Database Migration**: During container boot or via SSH terminal inside App Service, run `python manage.py migrate --noinput`.
4. **Validation**: Test the `/health/`, `/api/`, and `/admin/` endpoints directly against the Azure domain.
5. **GitHub CD Configuration**: Add Azure deployment targets sequentially to `.github/workflows/ci.yml` strictly for the `main` branch.

## 5. Rollback Strategy
- **Identified Failure**: Use Application Insights and App Service Log Stream to monitor `gunicorn` logs and 500 error spikes.
- **Rollback Process**: Do NOT immediately drop databases or `flush`. Re-deploy the previously known valid Docker tag from Azure Container Registry and perform a soft restart. Do not manually mutate migrations during rollback.
