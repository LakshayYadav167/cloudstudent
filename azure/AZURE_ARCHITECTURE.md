# PLANNED / DEMONSTRATION ARCHITECTURE

The Azure architecture for CloudStudent is designed around Azure App Service for Containers and Azure Database for PostgreSQL.

## Core Components
1. **Azure App Service (Web App for Containers):**
   - Hosts the Docker image containing Python 3.12, Django, Gunicorn, and WhiteNoise.
   - Handles SSL termination and load balancing.
   - Automatically injects configuration via App Settings (Environment Variables).

2. **Azure Database for PostgreSQL (Flexible Server):**
   - Managed PostgreSQL 15 instance.
   - High availability and automated backups.
   - Secure connection strictly restricted to the App Service subnet or Azure services.

3. **Azure Container Registry (ACR):**
   - Private registry to store the compiled Docker images pushed by GitHub Actions.

4. **GitHub Actions (CI/CD):**
   - Executes tests, Django checks, and builds the container.
   - Securely pushes the container to ACR using OpenID Connect (OIDC) or Service Principal credentials.
   - Triggers the App Service webhook to pull the latest image.

## Security Boundaries
- The PostgreSQL database is configured to reject public internet traffic.
- The App Service communicates with the database over encrypted SSL channels (`sslmode=require`).
- Secrets (like `SECRET_KEY`, `DATABASE_URL`) are exclusively stored in Azure App Settings and injected into the container at runtime.

*Note: This architecture is fully documented as a blueprint. To maintain a strict ₹0 budget, it is not currently provisioned.*
