# Azure Deployment Guide (Demonstration)

This guide outlines the theoretical steps to deploy CloudStudent to Azure. 

## 1. Prerequisites
- An active Azure Subscription.
- Azure CLI installed (`az`).
- Docker installed locally.

## 2. Infrastructure Provisioning (Theoretical)
```bash
# Set variables
RESOURCE_GROUP="rg-cloudstudent-prod"
LOCATION="eastus"
APP_NAME="app-cloudstudent-prod"
DB_SERVER="psql-cloudstudent-prod"

# Create Resource Group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create PostgreSQL Server
az postgres flexible-server create \
  --resource-group $RESOURCE_GROUP \
  --name $DB_SERVER \
  --admin-user <admin-username> \
  --admin-password <admin-password> \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 15

# Create App Service Plan
az appservice plan create \
  --name plan-cloudstudent \
  --resource-group $RESOURCE_GROUP \
  --is-linux \
  --sku B1

# Create Web App for Containers
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan plan-cloudstudent \
  --name $APP_NAME \
  --deployment-container-image-name <acr-name>.azurecr.io/cloudstudent:latest
```

## 3. Configuration Management
Apply the environment variables securely to the App Service:
```bash
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --settings \
    SECRET_KEY="<production-secret-key>" \
    DEBUG="False" \
    ALLOWED_HOSTS="$APP_NAME.azurewebsites.net" \
    CSRF_TRUSTED_ORIGINS="https://$APP_NAME.azurewebsites.net" \
    DATABASE_URL="postgres://<user>:<password>@<db-server>.postgres.database.azure.com:5432/cloudstudent?sslmode=require" \
    WEBSITES_PORT="8000"
```

## 4. Continuous Deployment
GitHub Actions is configured via the `.github/workflows/azure-deploy-demo.yml` blueprint. The pipeline pushes the Docker image to ACR and executes an Azure Webhook deployment to restart the container with the latest code.
