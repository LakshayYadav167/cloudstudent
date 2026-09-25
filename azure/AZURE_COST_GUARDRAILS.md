# Azure Cost Guardrails

This repository intentionally provisions ZERO Azure resources. 
This Azure material is a deployment demonstration and architecture blueprint.

## Provisioning Risk Assessment

| Resource | Status | Cost Risk | Reason |
|----------|--------|-----------|--------|
| App Service | Not provisioned | None | Documentation only |
| App Service Plan | Not provisioned | None | Documentation only |
| PostgreSQL | Not provisioned | None | Documentation only |
| Container Registry | Not provisioned | None | Documentation only |
| Application Insights | Not provisioned | None | Documentation only |
| Log Analytics | Not provisioned | None | Documentation only |
| VNet | Not provisioned | None | Documentation only |
| GitHub Actions | Existing | ₹0 under current public-standard configuration | CI only |

## Strict Cloud Operating Principles

- **Never enable Pay-As-You-Go** for this project.
- **Never add a payment method** to the Azure subscription for this project.
- **Never provision paid Azure infrastructure** directly from this repository without prior explicit approval and redesign.
- Azure credits or student trials **must not be treated as permission to spend money** or leave resources running.
- If a future deployment cannot remain safely free or within strict ₹0 boundaries, do not deploy it.
- **GitHub remains the permanent portfolio and source repository.** The codebase and CI pipeline represent the complete state of the engineering effort.
