# CloudStudent — Azure Deployment Demonstration

## Overview
CloudStudent includes a recruiter-ready Azure deployment architecture and CI/CD deployment blueprint. 
**Note: Azure resources are intentionally not provisioned in this repository to maintain a zero-cost development environment.**

## Why Azure
Azure App Service and Azure Database for PostgreSQL provide a highly scalable, enterprise-grade foundation for Django applications. This blueprint demonstrates how CloudStudent is technically prepared for a seamless transition from local containerized development to a production-grade cloud environment.

## Current Application Architecture
CloudStudent is currently built, tested, and verified using a production-ready containerized architecture (Python 3.12, Django 5.0, Gunicorn, PostgreSQL 15, and WhiteNoise). The CI pipeline running on GitHub Actions verifies this exact containerized environment against a robust test suite.

## Azure Target Architecture
The planned architecture leverages Azure App Service for Containers to host the Django application and Azure Database for PostgreSQL Flexible Server as the data backend. See the [Architecture Diagram](diagrams/azure-deployment-architecture.md) for details.

## Container Deployment Strategy
The existing `Dockerfile` requires zero modifications to run on Azure. Azure App Service will directly pull the built image and expose the application on the `$PORT` automatically injected by Azure, while WhiteNoise efficiently handles static file delivery.

## CI/CD Flow
A demonstration GitHub Actions workflow is provided in `.github/workflows/azure-deploy-demo.yml`. It outlines the exact steps required to push the Docker image to an Azure Container Registry and trigger a Webhook deployment on the App Service.

## Environment Configuration
Configuration is fully managed via standard environment variables (12-factor app methodology). All sensitive variables are designed to be securely injected via Azure App Settings. See [Environment Guide](AZURE_ENVIRONMENT.md) for details.

## Security
The application enforces `DEBUG=False`, secure headers, strictly managed `ALLOWED_HOSTS`, and Role-Based Access Controls. No credentials or secrets are committed to this repository.

## Cost Controls
Strict cost guardrails are documented in [Cost Guardrails](AZURE_COST_GUARDRAILS.md) to ensure that the project remains at a strict ₹0 out-of-pocket cost.

## Current Implementation Status
Currently, the CI pipeline is live and validating the application. Azure deployment architecture and CI/CD deployment blueprints are prepared but intentionally inactive.

## Future Deployment Path
If a live deployment is required, the documented templates can be hydrated with valid Azure Subscription credentials to provision the infrastructure and trigger the first live deployment.
