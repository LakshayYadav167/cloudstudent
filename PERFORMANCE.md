# CloudStudent Performance

This document outlines the specific optimizations applied to CloudStudent to ensure a responsive, highly performant experience even at scale.

## Database Query Strategy
The application has been heavily audited for the "N+1 Query Problem", an infamous ORM anti-pattern. 

## select_related / prefetch_related
CloudStudent relies aggressively on `select_related()` to execute fast SQL `JOIN` operations at the database level rather than triggering sequential lookups across the network.
- `Course` endpoints instantly join `instructor` details.
- `Enrollment` endpoints instantly join `student__user` and `course`.
- `AcademicRecord` endpoints instantly join all foreign keys down to the `user`.

## Pagination
API responses for all list endpoints are fundamentally bounded. The standard Django REST Framework `PageNumberPagination` restricts payloads to 10 records per page. Unbounded database `.all()` calls are structurally blocked from the internet.

## Search and Filtering
Full-text search queries via standard API parameters (`?search=CS101`) are pushed directly to PostgreSQL. They search indexed character fields exclusively (first name, last name, code) avoiding cross-table sequential scans where possible.

## Static Files
Static files (CSS, JS, Images) are NOT served by standard Django views. The application utilizes **WhiteNoise**, which wraps the WSGI application and serves heavily compressed, infinitely cacheable static assets natively through Gunicorn, entirely bypassing the database and Django routing layers.

## Docker Performance
The container is built dynamically upon the lightweight `python:3.12-slim` image, keeping memory consumption extremely minimal. Caching directories (e.g. `pip cache`) are bypassed during build.

## Gunicorn
The WSGI gateway uses optimized sync workers. The number of concurrent worker processes can easily be scaled vertically by modifying the `docker-compose.yml` startup command (`-w 4`).

## Database Connections
CloudStudent uses `dj_database_url` with connection health checks (`conn_health_checks=True`) and connection persistence (`conn_max_age=600`). This completely eliminates the TCP/IP overhead of negotiating a new PostgreSQL connection for every single HTTP request.

## Query Optimization
The Dashboard explicitly uses database-level aggregate functions (`Count`, `Avg`).
For example:
```python
AcademicRecord.objects.aggregate(Avg('marks'))['marks__avg']
```
This forces PostgreSQL to compute the mathematical average natively in C-code across the entire table, rather than pulling thousands of rows into Python memory to compute the average programmatically.

## Testing Method
Performance has been verified locally through standardized ORM metric evaluation. Explicit load testing (e.g. Locust, JMeter) is intentionally omitted from the standard CI/CD pipeline to avoid unnecessary Azure/Runner billing or network spam.

## Known Limitations
- We do not currently use Django's `cache` framework (Redis/Memcached). The database performs real-time queries for every request.
- Read replicas are not currently supported in the standard blueprint.
